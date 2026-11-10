# Unified statute coding database — dataset / codebook 0.3.0

The current first draft has **400 decisions, 773 evidence records, 24 jurisdictions and 25 comparison cases**. All decisions await team review; current legal force is unverified. La Rioja is secondary/higher only, and Neuquén/Río Negro national-reference clauses have unresolved provincial applicability. The count is coverage of supplied material, not proof of 24 comparable primary frameworks.

Start with [the searchable review page](statute_review.html) and [the consolidated pending issues](full_review.md). The review page contains filters, Spanish source pages and the open issue queue. Earlier [CABA](caba_review.md) and [Catamarca](catamarca_review.md) notes describe prior revisions.

## Current files

All tables are UTF-8 under `data/statute_coding/`:

| File | Purpose |
| --- | --- |
| `statute_coding.csv` | Main database: one decision per case × indicator. |
| `statute_evidence.csv` | Spanish excerpts/page context, joined on `row_id`. |
| `statute_documents.csv` | Source identity, path, page count and checksum; includes context-only sources. |
| `codebook.csv` | Current questions, descriptive categories and decision rules. |
| `statute_decisions.json` | Canonical curated decisions used to regenerate the tables and review page. |
| `pending_decisions.csv` | All 55 unclear and 35 not-found decisions, linked to issue records. |
| `review_queue.csv` | Open issues, priorities and next actions; provided decisions can also be affected. |
| `jurisdiction_coverage.csv` | Case counts, status counts, education scope and comparability notes. |
| `source_review_status.csv` | Cited-record counts, extraction status and source caveats. |
| `manual_transcriptions.json` | Four selected scan excerpts declared separately from automatic matching. |
| `statute_validation_report.json` | Structural/provenance checks and their limits. |
| `revision_log.csv` | Version changes and back-application record. |

Run `source("R/02_load_statute_pilot.R")`, then `View(statute_coding)` or `View(statute_pending)`. The loader needs no extra R packages. `statute_full` is an evidence-expanded join, not the unit for counting decisions. Rebuild with `scripts/export_statute_coding.py`; check with `scripts/validate_statute_coding.py` (requires pypdf).

The batch extends descriptive categories for course-versus-exam promotion, conditional examination routes, suspended appraisal, externally specified attendance additions, insufficient documentation and an explicit cessation exception. The existing 96 decisions and 213 excerpts are substantively unchanged. See [codebook changes](codebook_changes_0_3.md). Original `pilot_*`, `codebook_v0_1.csv` and `codebook_v0_2.csv` are historical snapshots.

New evidence often quotes the full cited PDF page to preserve context when headings or extraction order are unreliable. Article locators identify the relevant clause; adjacent provisions can occur in the quotation. Four manually transcribed excerpts were visually read and are not automatically text-matched. No finding has independent second-coder adjudication. Source matching does not verify the English interpretation, exhaustive absence, provincial applicability or current force.

---

## Original pilot protocol and snapshot documentation

# Provincial statute coding pilot

This first draft codes the supplied documents for Buenos Aires, Misiones and Córdoba against a common codebook. It is ready for team review, not a completed validation of the law currently in force. The pilot has 16 indicators, 64 decisions, 130 Spanish evidence excerpts and seven source PDFs.

## Start here

Open `pilot_review.html` for the searchable review table, or read `pilot_findings.md` for the initial comparison and questions to resolve. The review page is a local document; it does not update the earlier context website.

The pilot deliberately separates four comparison cases:

- `PBA_PRI`: primary education, applying the Buenos Aires statute's general provisions.
- `MIS_PRI`: primary education and the general provisions of the Misiones text.
- `COR_PRI`: Córdoba primary/initial provisions, where applicable.
- `COR_SEC`: Córdoba secondary provisions, including shared general rules in its middle/special/higher statute. Higher-education-specific provisions are not transferred to secondary teachers.

Córdoba is one province with two cases. Do not count the pilot as four provinces. Buenos Aires and Misiones secondary-specific chapters are outside this first comparison; they require later cases if the project expands beyond primary education. The common primary comparison is three provinces.

## Files and keys

The R-ready UTF-8 files are under `data/statute_coding/`:

| File | Unit and purpose |
| --- | --- |
| `codebook_v0_1.csv` | One row per indicator: question, permitted descriptive codes and decision rule. |
| `pilot_coding.csv` | One row per case × indicator. English finding, exceptions, confidence and review state. |
| `pilot_evidence.csv` | One row per excerpt, linked by `row_id`; source ID, article and one-based PDF page. |
| `pilot_documents.csv` | One row per supplied PDF: actual instrument, source type, relative path, page count, SHA-256 checksum and version caveats. |
| `pilot_decisions.json` | Canonical pilot decisions, codebook and evidence used to generate the CSVs and review page. |
| `review_queue.csv` | Specific unresolved questions and next actions. |
| `revision_log.csv` | Codebook changes and the cases affected. |
| `validation_report.json` | Structural, source, excerpt and coverage checks. |

Join coding to evidence on `row_id`, then to documents on `document_id`. One coding decision can have several evidence excerpts. Never count evidence rows as separate statutory observations.

## Coding protocol

1. Establish the province, education branch, employment status, instrument type, date and scope before coding. The applicable provision can be in an annex rather than the enacting law; specify that in the source description.
2. Read the full relevant provision and exceptions. Search keywords to navigate, not to decide the code automatically. Use a PDF page number counted from the start of the file, not an inferred printed page.
3. Record what the supplied text prescribes. Keep the English summary separate from the original Spanish excerpt. Quotes preserve extracted wording with whitespace normalized; extraction artifacts can remain in other source text.
4. Treat amended and repealed provisions explicitly. Do not revive a struck-out/repealed rule or assume a reference to another law supplies its contents. Specific amended clauses take precedence for the clause addressed, but consolidation is not an independent verification of current legal effect.
5. Use the descriptive code and the provision status together. Do not turn the statuses into scores. No code is a ranking of policy quality.
6. Add implementation evidence, literature benchmarks and policy recommendations in separate datasets later. A legal provision is not evidence of actual compliance or effectiveness.
7. Every first-pass row remains `awaiting_team_review`. Record reviewer initials, date and adjudication in a later version; confidence describes clarity of the supplied text, not validity of current law.

### Provision status

- `provided`: the supplied corpus contains an explicit relevant provision. This does not mean complete regulation, actual implementation or verified current force.
- `excluded`: a relevant entitlement or mechanism is expressly ruled out for the specified scope. Use only with an explicit exclusion; the present pilot has no rows using this status.
- `not_found`: the narrowly defined mechanism was not identified after reviewing the specified career/remuneration chapters and supplied supplements. Read the search scope and context evidence in the row. It does not mean the province has no such policy.
- `unclear`: delegation to missing instruments, repeal, conflict or insufficient detail prevents a reliable answer. Do not replace with zero or an assumed absence.

`direct_provision` evidence supports a positive or unresolved rule. `search_context` points to the closest relevant provisions for a `not_found` decision; a context quote does not itself prove legal absence. All rows have `legal_currency = not_verified` because this is coding of the provided corpus, not a current-law audit.

### Comparing seniority and merit

Keep entry ranking, promotion eligibility, competition scoring, periodic appraisal and salary components separate. A statute can use service years and appraisal together. Attendance/training-conditioned pay is not automatically teaching-performance pay. More teaching hours, a transfer, or a management post is not automatically a higher classroom-teacher rank.

## Versioning and the next province

Codebook version `0.1.0` is provisional. Review the questions in `review_queue.csv` first. Add the next province using the same indicators and branch definitions. If it reveals a missing category, revise the codebook and log the change, then review every affected earlier case before making comparisons. Preserve old versions rather than silently changing meanings.

No aggregate index or province ranking is calculated. A second human review of the evidence is still needed; this pilot does not claim inter-coder agreement.

## Reproduce and load in R

Open the RStudio project and run:

```r
source("R/02_load_statute_pilot.R")
```

This loads the codebook, coding, evidence and document inventory, checks keys and produces `statute_pilot_full`, a long table with source references. To rebuild the exported tables and review page after editing canonical decisions, run `scripts/export_statute_pilot.py` using Python 3. That exporter does not recode the laws automatically. The evidence-validation script additionally needs `pypdf`.

The source PDFs stay in ignored local raw-data folders. The original Dropbox ZIP places Misiones inside Mendoza. Its canonical path in this pilot is `data/raw/statutes/Misiones/`; the R loader also recognizes the original archive location so teammates can review the same source without moving it first.

Dataset revision 0.1.1 clarifies Córdoba article 67, the amendment/repeal distinction around article 72, and the Economy Ministry resolution conditions. Indicator definitions remain codebook 0.1.0. Original archive filenames are retained in `archive_source_file`; the R loader and validator recognize these aliases.
