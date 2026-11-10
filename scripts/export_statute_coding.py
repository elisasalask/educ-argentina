"""Export curated coding decisions. This does not code legal texts automatically."""
from pathlib import Path
import csv,json,html,urllib.parse,collections
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/statute_coding'
P=json.loads((DATA/'statute_decisions.json').read_text())
def export(name,items):
 with (DATA/name).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(items[0]),lineterminator='\n');w.writeheader();w.writerows(items)
for name,key in [('codebook.csv','codebook'),('statute_coding.csv','coding'),('statute_evidence.csv','evidence')]:export(name,P[key])
if 'documents' in P:export('statute_documents.csv',P['documents'])
# Refresh review aids from the same canonical decisions and maintained issue queue.
queue=list(csv.DictReader((DATA/'review_queue.csv').open(encoding='utf-8')))
pending=[]
for r in P['coding']:
 if r['provision_status'] not in ('unclear','not_found'):continue
 linked=[q['issue_id'] for q in queue if (q['case_ids']=='all' or r['case_id'] in q['case_ids'].split(';')) and (q['affected_indicators'] in ('all','all rows') or r['indicator_id'] in q['affected_indicators'].split(';'))]
 pending.append(dict(row_id=r['row_id'],province=r['province'],indicator=r['indicator'],provision_status=r['provision_status'],reason=r['summary_en'],limits=r['exceptions_and_limits'],issue_ids=';'.join(linked),review_state=r['review_state']))
if pending:export('pending_decisions.csv',pending)
coverage=[]
for prov in sorted({r['province'] for r in P['coding']}):
 rr=[r for r in P['coding'] if r['province']==prov];cases=list(dict.fromkeys(r['case_id'] for r in rr));counts=collections.Counter(r['provision_status'] for r in rr)
 coverage.append(dict(province=prov,case_ids=';'.join(cases),decisions=len(rr),provided=counts['provided'],excluded=counts['excluded'],unclear=counts['unclear'],not_found=counts['not_found'],education_scope='; '.join(dict.fromkeys(r['education_scope'] for r in rr)),scope_notes=' '.join(P.get('case_notes',{}).get(c,'') for c in cases).strip(),review_state='awaiting_team_review'))
export('jurisdiction_coverage.csv',coverage)
if (DATA/'source_review_status.csv').exists():
 status=list(csv.DictReader((DATA/'source_review_status.csv').open(encoding='utf-8')))
 for source in status:source['cited_excerpts']=sum(e['document_id']==source['document_id'] for e in P['evidence'])
 export('source_review_status.csv',status)

sources={x['document_id']:x for x in csv.DictReader((DATA/'statute_documents.csv').open())}
evidence={}
for e in P['evidence']:evidence.setdefault(e['row_id'],[]).append(e)
esc=lambda x:html.escape(str(x))
sections=[]
for r in P['coding']:
 excerpts=[]
 for e in evidence[r['row_id']]:
  d=sources[e['document_id']];href='../../'+urllib.parse.quote(d['source_file'])+'#page='+str(e['pdf_page'])
  excerpts.append(f'<div class="evidence"><a href="{href}" target="_blank">{esc(e["document_id"])} · PDF p. {e["pdf_page"]} · {esc(e["article"])}</a><small>{esc(e["evidence_role"].replace("_"," "))} · {esc(d["instrument_type"].replace("_"," "))}</small><blockquote lang="es">{esc(e["excerpt_es"])}</blockquote></div>')
 attrs=' '.join(f'data-{k}="{esc(r[k])}"' for k in ['case_id','dimension','provision_status'])
 search=esc(' '.join(str(v) for v in r.values()))
 sections.append(f'''<article {attrs} data-search="{search}"><div class="rowhead"><span>{esc(r['case_id'])} / {esc(r['indicator_id'])}</span><span class="badge {r['provision_status']}">{esc(r['provision_status'].replace('_',' '))}</span></div><h3>{esc(r['indicator'])}</h3><p>{esc(r['summary_en'])}</p><p class="notes"><strong>Exceptions and limits:</strong> {esc(r['exceptions_and_limits'])}</p><details><summary>Spanish evidence and source pages ({len(excerpts)})</summary>{''.join(excerpts)}</details><div class="meta">Code: {esc(r['coded_value'])} · Interpretation confidence: {r['text_interpretation_confidence']} · Team review pending · Current legal force unverified</div></article>''')
case_names={case:f"{spec[0]} · {'Secondary / higher' if case.endswith('_SEC') else 'Primary'}" for case,spec in P['cases'].items()}
case_names['COR_SEC']='Córdoba · Secondary extension'
opts=lambda key:''.join(f'<option value="{esc(x)}">{esc(case_names.get(x,x.replace("_"," ")))}</option>' for x in sorted(set(r[key] for r in P['coding'])))
book=''.join(f'<tr><td>{esc(c["indicator_id"])}</td><td>{esc(c["indicator"])}</td><td>{esc(c["decision_rule"])}</td></tr>' for c in P['codebook'])
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Statute coding review</title><style>
*{box-sizing:border-box}body{margin:0;background:#f6f5f1;color:#172c40;font:16px/1.6 Arial,sans-serif}main{max-width:1100px;margin:auto;padding:40px 24px}h1,h2{font-family:Georgia,serif;font-weight:normal;line-height:1.15}h1{font-size:44px;margin:10px 0 20px}h2{font-size:30px}h3{font-size:19px;margin:12px 0}.eyebrow{font-size:11px;letter-spacing:2px;color:#145bc4;font-weight:bold}.intro{font-size:18px;max-width:830px}.notice{background:#fff0cf;border-left:4px solid #ba8c24;padding:15px 20px;margin:20px 0;font-size:14px}.links{display:flex;gap:18px;flex-wrap:wrap;font-size:13px}a{color:#1359b5}.controls{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;padding:20px;background:#e6edf6;margin-top:30px}.controls label{display:block;font-size:12px;font-weight:bold}.controls select,.controls input{width:100%;padding:10px;background:white;border:1px solid #b2c0cf;font:inherit;color:#172c40}.search{grid-column:1/-1}article{background:white;border:1px solid #cfd8e1;margin:18px 0;padding:24px}.rowhead{display:flex;justify-content:space-between;gap:15px;font-size:12px;letter-spacing:.3px;font-weight:bold}.badge{padding:2px 9px;border-radius:3px;background:#e6f2ed;color:#116448}.badge.unclear{background:#fff0cf;color:#705400}.badge.not_found{background:#edf0f4;color:#4c5c6f}.notes{font-size:14px;color:#526477}.meta{border-top:1px solid #e0e5eb;padding-top:12px;margin-top:16px;font-size:11px;color:#607183;overflow-wrap:anywhere}summary{cursor:pointer;font-size:14px;font-weight:bold}.evidence{padding:15px 0;border-bottom:1px solid #e1e6ec}.evidence small{display:block;color:#697988;font-size:11px}blockquote{margin:8px 0;padding:8px 16px;background:#f3f6fa;font-family:Georgia,serif;font-size:16px;border-left:3px solid #7b9cc6}table{width:100%;border-collapse:collapse;font-size:13px}td,th{border:1px solid #cad3dc;padding:10px;text-align:left;vertical-align:top}.count{font-size:14px;color:#526477}[hidden]{display:none!important}button{font:inherit;padding:7px 14px;cursor:pointer;border:1px solid #95aac3;background:white;color:#172c40}select:focus-visible,input:focus-visible,button:focus-visible,a:focus-visible{outline:3px solid #236dd4;outline-offset:3px}.tablewrap{overflow-x:auto}@media(max-width:650px){.controls{grid-template-columns:1fr}.search{grid-column:auto}h1{font-size:34px}article{padding:18px}.rowhead{font-size:10px}}@media print{.controls,.links{display:none}article{break-inside:avoid}details{display:block}body{background:white}}</style></head><body><main><div class="eyebrow">ARGENTINA / MODEL TEACHER STATUTE / CODING 0.2.0</div><h1>What do the supplied statutes prescribe?</h1><p class="intro">Draft coding for Buenos Aires, Misiones, Córdoba and CABA. The common comparison is primary education; Córdoba secondary is kept as a separate extension.</p><div class="notice"><strong>Draft for team review.</strong> 16 indicators · 80 coding decisions · 124 Spanish excerpts · 9 PDFs. These are formal provisions from documents supplied for the assignment. Current legal force and implementation are not verified. “Not found” does not mean a policy does not exist.</div><div class="links"><a href="pilot_findings.md">Read the initial pilot comparison</a><a href="README.md">Coding protocol</a><a href="../../data/statute_coding/statute_coding.csv">Coding table (CSV)</a><a href="../../data/statute_coding/statute_evidence.csv">Evidence table (CSV)</a><a href="../../data/statute_coding/review_queue.csv">Review queue (CSV)</a></div><div class="controls"><div><label for="case">Comparison case</label><select id="case"><option value="">All five cases</option>CASE_OPTIONS</select></div><div><label for="dimension">Dimension</label><select id="dimension"><option value="">All four dimensions</option>DIM_OPTIONS</select></div><div><label for="status">Provision status</label><select id="status"><option value="">All statuses</option>STATUS_OPTIONS</select></div><div class="search"><label for="search">Search findings, codes or article notes</label><input id="search" type="search" placeholder="e.g. appraisal, seniority, substitute, Law 10237"></div></div><p class="count" id="count" aria-live="polite"></p><button id="reset">Reset filters</button><section id="rows">ROWS</section><h2>Codebook at a glance</h2><p>Codes describe mechanisms, not policy quality. See the CSV codebook and protocol for permitted values and status definitions.</p><div class="tablewrap"><table><thead><tr><th>Code</th><th>Indicator</th><th>Decision rule</th></tr></thead><tbody>BOOK</tbody></table></div><p class="count">PDF links open local source files; data and evidence remain on your computer. No source PDFs are embedded in this document.</p></main><script>
const ids=['case','dimension','status','search'];function filter(){const c=document.getElementById('case').value,d=document.getElementById('dimension').value,s=document.getElementById('status').value,q=document.getElementById('search').value.toLocaleLowerCase();let n=0;document.querySelectorAll('#rows article').forEach(r=>{r.hidden=!!((c&&r.dataset.case_id!==c)||(d&&r.dataset.dimension!==d)||(s&&r.dataset.provision_status!==s)||(q&&!r.dataset.search.toLocaleLowerCase().includes(q)));if(!r.hidden)n++});document.getElementById('count').textContent=n+' of 80 coding decisions shown.'}ids.forEach(id=>document.getElementById(id).addEventListener('input',filter));document.getElementById('reset').onclick=()=>{ids.forEach(id=>document.getElementById(id).value='');filter()};filter();</script></body></html>'''
page=page.replace('124 Spanish excerpts',str(len(P['evidence']))+' Spanish excerpts')
page=page.replace('16 indicators',str(len(P['codebook']))+' indicators')
page=page.replace('80 coding decisions',str(len(P['coding']))+' coding decisions')
page=page.replace('9 PDFs',str(len(P['documents']))+' PDFs')
page=page.replace('All five cases','All comparison cases')
page=page.replace('CODING 0.2.0','CODEBOOK '+esc(P['codebook_version'])+' / DATASET '+esc(P['dataset_revision']))
jurisdictions=', '.join(sorted({r['province'] for r in P['coding']}))
page=page.replace('Draft coding for Buenos Aires, Misiones, Córdoba and CABA.', 'Draft coding for '+esc(jurisdictions)+'.')
latest=P.get('latest_review_case')
if latest:
 label=case_names[latest]
 notes=esc(P['latest_review_notes'])
 page=page.replace('<div class="links">','<div class="notice"><strong>Latest addition: '+esc(label)+'.</strong> Review one jurisdiction at a time. <a href="'+notes+'">Read the latest review notes</a>.</div><div class="links">',1)
# A case-specific link opens the existing review with the relevant filter selected.
page=page.replace(";filter();</script>",";const initialCase=new URLSearchParams(location.hash.slice(1)).get('case');if(initialCase&&[...document.getElementById('case').options].some(o=>o.value===initialCase))document.getElementById('case').value=initialCase;filter();</script>")
page=page.replace('The common comparison is primary education; Córdoba secondary is kept as a separate extension.', 'There are 25 comparison cases across 24 jurisdictions. La Rioja covers secondary/higher education only; its primary framework is missing. Neuquén and Río Negro national-reference findings remain conditional on provincial applicability. Córdoba includes separate primary and secondary cases.')
page=page.replace(str(len(P['documents']))+' PDFs',str(len(P['documents']))+' supplied source files (including context-only and scanned documents)')
page=page.replace('<div class="links">','<div class="notice"><strong>All-jurisdiction first draft complete.</strong> Findings await team review. <a href="full_review.md">Read the consolidated pending issues</a> · <a href="../../data/statute_coding/pending_decisions.csv">Unclear and not-found decisions</a> · <a href="../../data/statute_coding/jurisdiction_coverage.csv">Coverage by jurisdiction</a>.</div><div class="links">',1)
page=page.replace('CASE_OPTIONS',opts('case_id')).replace('DIM_OPTIONS',opts('dimension')).replace('STATUS_OPTIONS',opts('provision_status')).replace('ROWS',''.join(sections)).replace('<tbody>BOOK</tbody>','<tbody>'+book+'</tbody>')
queue=list(csv.DictReader((DATA/'review_queue.csv').open(encoding='utf-8')))
issues=''.join('<tr><td>'+esc(q['issue_id'])+'<br>'+esc(q['priority'])+'</td><td>'+esc(q['case_ids'])+'<br><strong>'+esc(q['topic'])+'</strong></td><td>'+esc(q['reason'])+'<br><strong>Next:</strong> '+esc(q['next_action'])+'</td></tr>' for q in queue if q['status']=='open')
page=page.replace('<h2>Codebook at a glance</h2>','<h2 id="pending">Pending issues for team review</h2><p>These issues can affect several rows. The linked pending-decisions CSV lists every unclear/not-found decision; all other draft decisions also await team review.</p><details><summary>Open '+str(len(queue))+' issue records</summary><div class="tablewrap"><table><thead><tr><th>Issue / priority</th><th>Scope / topic</th><th>Reason / next action</th></tr></thead><tbody>'+issues+'</tbody></table></div></details><h2>Codebook at a glance</h2>')
(ROOT/'docs/statute_coding/statute_review.html').write_text(page,encoding='utf-8')
print('Exported unified tables and local review document.')
