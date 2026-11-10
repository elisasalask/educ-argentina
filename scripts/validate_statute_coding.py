"""Validate unified coding structure and quote provenance, not legal truth."""
from pathlib import Path
import csv,json,re,hashlib,collections
from pypdf import PdfReader
root=Path(__file__).resolve().parents[1];d=root/'data/statute_coding'
load=lambda name:list(csv.DictReader((d/name).open(encoding='utf-8')))
rows=load('statute_coding.csv');ev=load('statute_evidence.csv');docs=load('statute_documents.csv');book=load('codebook.csv')
master=json.loads((d/'statute_decisions.json').read_text())
errors=[]
def check(ok,message):
 if not ok:errors.append(message)
check(len(rows)==len(master['cases'])*len(book),'Expected one decision per case and indicator.')
check({r['case_id'] for r in rows}==set(master['cases']),'Cases do not match canonical master.')
for name,exported in [('coding',rows),('evidence',ev),('documents',docs),('codebook',book)]:
 expected=[{k:str(v) for k,v in item.items()} for item in master[name]]
 check(exported==expected,'CSV export differs from canonical '+name)
check(len({r['row_id'] for r in rows})==len(rows),'Duplicate coding keys.')
check(len({e['evidence_id'] for e in ev})==len(ev),'Duplicate evidence IDs.')
check(len({r['province'] for r in rows})==len({spec[0] for spec in master['cases'].values()}),'Jurisdiction coverage differs from master.')
check(len({doc['document_id'] for doc in docs})==len(docs),'Duplicate document IDs.')
for c in {r['case_id'] for r in rows}:
 check({r['indicator_id'] for r in rows if r['case_id']==c}=={b['indicator_id'] for b in book},'Incomplete indicator coverage: '+c)
source={};source_paths={}
for doc in docs:
 p=root/doc['source_file']
 if not p.exists() and doc.get('archive_source_file'):p=root/doc['archive_source_file']
 check(p.exists(),'Missing PDF '+str(p))
 if not p.exists():continue
 check(hashlib.sha256(p.read_bytes()).hexdigest()==doc['sha256'],'Changed PDF '+str(p))
 reader=PdfReader(p);check(len(reader.pages)==int(doc['pages']),'Page count mismatch '+doc['document_id'])
 source[doc['document_id']]=reader;source_paths[doc['document_id']]=str(p.relative_to(root))
norm=lambda s:re.sub(r'\s+',' ',s).strip()
ids={r['row_id'] for r in rows};bid={b['indicator_id']:b for b in book}
for r in rows:
 check(r['provision_status'] in ['provided','excluded','not_found','unclear'],'Invalid status '+r['row_id'])
 check(r['coded_value'] in bid[r['indicator_id']]['permitted_values'].split(';'),'Invalid descriptive code '+r['row_id'])
 check(r['review_state']=='awaiting_team_review','Unexpected reviewed claim '+r['row_id'])
 check(r['codebook_version']==master['codebook_version'],'Mixed codebook versions '+r['row_id'])
 check(r['legal_currency']=='not_verified','Unexpected claim of verified legal force '+r['row_id'])
 refs={e['evidence_id'] for e in ev if e['row_id']==r['row_id']}
 check(refs==set(r['evidence_ids'].split(';')),'Broken evidence links '+r['row_id'])
 if r['provision_status']=='not_found':check(all(e['evidence_role']=='search_context' for e in ev if e['row_id']==r['row_id']),'Absence falsely treated as direct evidence')
manual={e['evidence_id']:e for e in json.loads((d/'manual_transcriptions.json').read_text())} if (d/'manual_transcriptions.json').exists() else {}
page_text={}
manual_count=0
for e in ev:
 check(e['row_id'] in ids,'Orphan evidence '+e['evidence_id'])
 reader=source.get(e['document_id']);page=int(e['pdf_page'])
 check(reader is not None,'Unknown document '+e['document_id'])
 if reader is None:continue
 check(1<=page<=len(reader.pages),'Invalid page '+e['evidence_id'])
 if 1<=page<=len(reader.pages):
  if e['evidence_role']=='manual_transcription':
   record=manual.get(e['evidence_id'],{})
   check(all(str(record.get(k))==str(v) for k,v in e.items()),'Missing/mismatched manual transcription manifest '+e['evidence_id'])
   manual_count+=1
  else:
   key=(e['document_id'],page)
   if key not in page_text:page_text[key]=norm(reader.pages[page-1].extract_text() or '')
   check(norm(e['excerpt_es']) in page_text[key],'Quote mismatch '+e['evidence_id'])
pending=load('pending_decisions.csv');coverage=load('jurisdiction_coverage.csv');queue=load('review_queue.csv')
check({r['row_id'] for r in pending}=={r['row_id'] for r in rows if r['provision_status'] in ('unclear','not_found')},'Pending-decision coverage mismatch')
check(len(pending)==len({r['row_id'] for r in pending}),'Duplicate pending decisions')
check(len(coverage)==24 and sum(int(r['decisions']) for r in coverage)==len(rows),'Jurisdiction coverage totals mismatch')
check({r['province'] for r in coverage}=={r['province'] for r in rows},'Coverage jurisdiction names mismatch')
qids={q['issue_id'] for q in queue}
for r in pending:check(set(r['issue_ids'].split(';'))<=qids,'Broken issue link '+r['row_id'])
for r in rows:
 if r['case_id']=='RNE_PRI' or (r['case_id']=='NQN_PRI' and r['indicator_id'] not in ('PR04','CT03')):
  check(r['provision_status']=='unclear','National candidate incorrectly treated as settled provincial rule '+r['row_id'])

report=dict(coded_date=master['coded_date'],codebook_version=master['codebook_version'],dataset_revision=master['dataset_revision'],coding_decisions=len(rows),evidence_excerpts=len(ev),automatically_matched_excerpts=len(ev)-manual_count,manual_transcriptions_requiring_second_review=manual_count,documents=len(docs),provinces=len({r['province'] for r in rows}),comparison_cases=len(master['cases']),status_counts=dict(collections.Counter(r['provision_status'] for r in rows)),checks_passed=not errors,errors=errors,checks=['Case/indicator completeness against canonical master','CSV exports match canonical decisions','Keys and joins, including pending decisions and issue links','Jurisdiction coverage and conditional national-reference status','Permitted status and descriptive codes','PDF existence, SHA-256 and page count','Exact whitespace-normalized extractable excerpt on cited PDF page; manual transcriptions checked against declared manifest separately'],selected_pages_visually_inspected=master.get('selected_pages_visually_inspected',[]),limitations=['Source matching does not validate English interpretations or prove absence.','No independent second coder or adjudication; manual scan transcriptions are not automatically verified.','Current legal force and completeness of external regulations not verified.'])
(d/'statute_validation_report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if errors:raise SystemExit(1)
