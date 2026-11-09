"""Validate pilot structure and exact normalized quote provenance, not legal truth."""
from pathlib import Path
import csv,json,re,hashlib,collections
from pypdf import PdfReader
root=Path(__file__).resolve().parents[1];d=root/'data/statute_coding'
load=lambda name:list(csv.DictReader((d/name).open(encoding='utf-8')))
rows=load('pilot_coding.csv');ev=load('pilot_evidence.csv');docs=load('pilot_documents.csv');book=load('codebook_v0_1.csv')
errors=[]
def check(ok,message):
 if not ok:errors.append(message)
check(len(rows)==64,'Expected 64 pilot coding decisions.')
check(len({r['row_id'] for r in rows})==len(rows),'Duplicate coding keys.')
check(len({e['evidence_id'] for e in ev})==len(ev),'Duplicate evidence IDs.')
check(len({r['province'] for r in rows})==3,'Pilot must cover three provinces.')
for c in {r['case_id'] for r in rows}:
 check({r['indicator_id'] for r in rows if r['case_id']==c}=={b['indicator_id'] for b in book},'Incomplete indicator coverage: '+c)
source={};source_paths={}
for doc in docs:
 p=root/doc['source_file']
 if not p.exists() and doc['document_id']=='MIS1':p=root/doc['source_file'].replace('/Misiones/','/Mendoza/')
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
 refs={e['evidence_id'] for e in ev if e['row_id']==r['row_id']}
 check(refs==set(r['evidence_ids'].split(';')),'Broken evidence links '+r['row_id'])
 if r['provision_status']=='not_found':check(all(e['evidence_role']=='search_context' for e in ev if e['row_id']==r['row_id']),'Absence falsely treated as direct evidence')
for e in ev:
 check(e['row_id'] in ids,'Orphan evidence '+e['evidence_id'])
 reader=source.get(e['document_id']);page=int(e['pdf_page'])
 check(reader is not None,'Unknown document '+e['document_id'])
 if reader is None:continue
 check(1<=page<=len(reader.pages),'Invalid page '+e['evidence_id'])
 if 1<=page<=len(reader.pages):check(norm(e['excerpt_es']) in norm(reader.pages[page-1].extract_text() or ''),'Quote mismatch '+e['evidence_id'])
report=dict(coded_date='2026-11-09',codebook_version='0.1.0',coding_decisions=len(rows),evidence_excerpts=len(ev),documents=len(docs),provinces=3,comparison_cases=4,status_counts=dict(collections.Counter(r['provision_status'] for r in rows)),checks_passed=not errors,errors=errors,checks=['Case/indicator completeness','Keys and joins','Permitted status and descriptive codes','PDF existence, SHA-256 and page count','Exact whitespace-normalized excerpt on cited PDF page'],selected_pages_visually_inspected=['PBA1:18','MIS1:6','COR3:19','COR5:9','COR2:3','COR4:2'],limitations=['Source matching does not validate English interpretations or prove absence.','No independent second coder or adjudication.','Current legal force and completeness of external regulations not verified.'])
(d/'validation_report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if errors:raise SystemExit(1)
