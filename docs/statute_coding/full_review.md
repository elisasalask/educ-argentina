# All-jurisdiction draft and pending review

Dataset 0.3.0 · Codebook 0.3.0 · Coded 9 November 2026

The first pass now contains **400 decisions across 24 jurisdictions and 25 cases**, using 16 indicators in the four assignment dimensions. There are **773 linked Spanish evidence records** and 51 supplied source files in the document inventory. An evidence record is not a separate observation; several records can quote the same PDF page. Some inventory sources are duplicates or context-only documents, not independently coded statutes.

Open [the searchable review page](statute_review.html), [the decision table](../../data/statute_coding/statute_coding.csv), or [the pending-decision list](../../data/statute_coding/pending_decisions.csv). The review page also includes the issue queue below the findings.

## What is ready

- A first draft for all 19 jurisdictions remaining after Catamarca, added to the existing five jurisdictions.
- The earlier 96 findings and 213 evidence records are preserved; their common codebook version is updated, without changing substantive codes or interpretations.
- 310 decisions have an explicit supplied provision, 55 remain unclear, and 35 record a mechanism not identified in the reviewed material. Every decision still awaits team review.
- R-ready decision, evidence, document and codebook tables, plus coverage and source-review inventories.
- Source checks for PDF hashes, page references, joins and extractable quotations. Four manually transcribed scan excerpts are declared separately and require independent checking. These checks do not adjudicate legal meaning.

## Scope before comparison

**These are not 24 fully comparable primary statutes.** La Rioja's supplied Law 5289 covers secondary/higher education, so its primary framework is still missing. Neuquén and Río Negro use national-reference candidate clauses whose provincial applicability remains unresolved; the explicitly provincial Neuquén supplement is identified separately. Santa Cruz has a supplied adoption law, subject to its non-conflict clause and later adaptations. Córdoba retains separate primary and secondary cases. Other jurisdictions' secondary-specific rules have not been comprehensively coded.

The task is to distinguish formal rules from school practice. This database codes the supplied formal texts only; implementation gaps require separate evidence. Document dates vary, and the coding date does not establish the law in force on that date. Do not calculate a province ranking, average raw category codes, count not-found as zero, or treat missing documentation as policy absence.

## Suggested review sequence

1. Agree the legal reference date and the education scope of the memo.
2. Resolve missing primary coverage and national-adoption questions: La Rioja, Neuquén and Río Negro.
3. Obtain missing cross-referenced instruments, especially Córdoba Law 10237, Entre Ríos Law 4065, Mendoza Decree 228/2016, and Santa Fe's employment/pay/appraisal framework.
4. Review incentive periods, protected absences and amounts, plus La Pampa's suspended appraisal provisions and Tierra del Fuego's scanned leave framework.
5. Second-check manual scan quotations and unusual historical clauses, including Santiago del Estero's appraisal-cessation exception.
6. Review every unclear and not-found row, then adjudicate the other draft findings. Record reviewer, date, reasoning and any back-application when changing the codebook.

## Open issue queue

Each issue can affect several decisions. Original pilot/CABA/Catamarca issues remain open; the new batch adds issues Q17–Q34. The row-linked pending file contains all 90 unclear/not-found decisions; provided rows can also have an open issue.

### Q01 · High · Legal reference date

Scope: `all`. Indicators: `all rows`.

Fix a shared legal reference date; distinguish document date from coding date.

Next action: Choose an as-of date, then obtain official current or historical consolidations for that date.

### Q02 · High · Leadership competition framework

Scope: `COR_PRI;COR_SEC`. Indicators: `PR01;PR02;MP02`.

Article 67 retains basic promotion rules and thresholds. Articles 70,71,73–77 are marked repealed, while amended article72 refers to Law10237 article10; the full law is still to obtain.

Next action: Obtain full Law 10237 and applicable implementing regulations; recode affected promotion indicators.

### Q03 · High · Seniority pay not recoverable

Scope: `COR_PRI;COR_SEC`. Indicators: `PR03`.

Remuneration articles are marked repealed and the prefaces refer to Decree 1001/14.

Next action: Obtain operative pay framework and relevant agreements; do not use zero for missing seniority schedules.

### Q04 · High · Resolution 7/2024 timing and exceptions

Scope: `COR_PRI;COR_SEC`. Indicators: `PR04`.

Pay conditions begin in 2024 and may subsequently change.

Next action: Confirm the chosen-period text, protected leave, exclusions, proportionality and later amendments.

### Q05 · Medium · Advanced classroom-stage definition

Scope: `all`. Indicators: `MP04`.

Current definition excludes more hours, location/category changes and coordinator roles.

Next action: Team to confirm definition or add a separate coordinator/mentoring indicator; back-apply any change.

### Q06 · High · Post-specific promotion thresholds

Scope: `PBA_PRI`. Indicators: `PR02`.

Article 80(d) delegates post-specific requirements.

Next action: Obtain the applicable regulation; retain unclear rather than zero years.

### Q07 · High · Leave and employment status

Scope: `all`. Indicators: `CT03`.

Supplied leave coverage is uneven; Córdoba booklet is union guidance.

Next action: Obtain primary leave laws and implementing rules; separate statutory rights, discretion and guidance.

### Q08 · High · Misiones consolidation and age restrictions

Scope: `MIS_PRI`. Indicators: `AS01;all MIS_PRI rows`.

Unofficial reproduction has no clear consolidation date and prints historical eligibility restrictions.

Next action: Match to an official consolidation for the agreed reference date; retain printed article numbering and former-number notes.

### Q09 · Medium · Substitute coverage timing

Scope: `COR_PRI`. Indicators: `CT04`.

Article 30 says same-day possession, while article 33 distinguishes mandatory coverage over eight days and shorter absences.

Next action: Review regulations and interpretation of the two clauses; keep their different functions separate.

### Q10 · Medium · Scope and empirical linkage

Scope: `all`. Indicators: `all rows`.

Primary is comparable across three provinces; Córdoba secondary is a separate extension.

Next action: Confirm primary focus and link to education datasets only after matching date, level and sector.

### Q11 · High · Second human review

Scope: `all`. Indicators: `all rows`.

This is a first coding pass, not a double-coded or adjudicated dataset.

Next action: A team member checks cited provisions and exceptions, records initials/date and resolves differences.

### Q12 · High · Adopting instrument for 2026 annex

Scope: `CABA_PRI`. Indicators: `AS04;PR01;CT02;CT04`.

Supplied annex has blank adopting-act number/date and differs from the 2022 regulation.

Next action: Obtain official adopting instrument and establish reference date before resolving appraisal cessation and course scoring.

### Q13 · Medium · Training salary authorization versus implemented scheme

Scope: `CABA_PRI`. Indicators: `PR04`.

Article 78 permits salary incentives but does not establish an amount or operational payment scheme.

Next action: Obtain implementing salary instruments if comparing actual pay incentives.

### Q14 · High · Law 5103 competition bases and implementing rules

Scope: `CAT_PRI`. Indicators: `PR01;PR02;MP02`.

Law5103 is supplied at PDF pp140–142 and suspends conflicting older promotion provisions; numeric service and appraisal requirements cannot be settled from the old articles alone.

Next action: Obtain implementing regulation and relevant primary leadership competition bases; resolve experience and appraisal criteria before comparison.

### Q15 · High · Historical stability and entry restrictions

Scope: `CAT_PRI`. Indicators: `AS01;AS03`.

Compilation prints old age/nationality/domicile conditions and transitory article173, while the later disciplinary regulation affirms titular stability.

Next action: Establish the legal reference date and obtain authoritative consolidated rules; check Law3090 and status of printed entry restrictions.

### Q16 · Medium · Training points and leave detail

Scope: `CAT_PRI`. Indicators: `CT02;CT03`.

Course recognition and paid study-leave rights are supplied, but complete points grid and detailed leave framework are not.

Next action: Obtain points regulation and applicable full leave regime if numeric comparison is required.

### Q17 · High · Reference date and legal applicability

Scope: `all`. Indicators: `all`.

All 24 are first-pass document-based drafts; no contemporary-force verification.

Next action: Fix the analysis reference date and verify official amendments before policy comparison.

### Q18 · High · Missing primary statute

Scope: `LRJ_SEC`. Indicators: `all`.

Law5289 is secondary/higher scope; no primary case has been invented.

Next action: Obtain and code the primary/general career framework.

### Q19 · High · National-text applicability

Scope: `NQN_PRI;RNE_PRI`. Indicators: `all`.

National Law14473 copies do not establish provincial adoption or adaptations; baseline findings are conditional.

Next action: Obtain provincial adoption/consolidation and amendments; resolve every conditional national-reference row.

### Q20 · High · Incomplete employment and pay framework

Scope: `SFE_PRI`. Indicators: `AS03;AS04;PR03;MP01;MP02;MP03`.

Supplied school/career regulations do not establish complete tenure, dismissal, annual appraisal or salary rules.

Next action: Obtain the general employment, disciplinary, concept and remuneration instruments.

### Q21 · High · Attendance incentive expiration

Scope: `SFE_PRI`. Indicators: `PR04`.

Decree586/2024 states a one-year term from16April2024.

Next action: Obtain any extension and date-specific amounts; retain historical coding until then.

### Q22 · High · Item Aula original instrument

Scope: `MEN_PRI`. Indicators: `PR04`.

Decree989/2016 modifies eligibility/exceptions; original Decree228/2016 is missing.

Next action: Obtain original decree and amendments, amount/denominator and reference-period conditions.

### Q23 · High · Appraisal suspension and compilation inconsistencies

Scope: `LPA_PRI`. Indicators: `MP01;MP02;PR03;PR04`.

Union compilation marks appraisal provisions suspended, while other annual duties remain printed; remuneration typography also needs checking.

Next action: Verify official suspension/extension instruments and correct seniority schedule/attendance wording.

### Q24 · High · Scanned adoption and board amendment

Scope: `SCR_PRI`. Indicators: `all`.

Law1023 adoption was manually transcribed; Law3350 is a scanned board amendment.

Next action: Second-check adoption against the scan and verify complete provincial adaptations; the supplied board amendment was visually reviewed.

### Q25 · High · Scanned leave framework and repealed provision

Scope: `TDF_PRI`. Indicators: `CT03`.

Decree1014/2014 leave source is scanned; Law728 is repealed by Law911 article17.

Next action: Transcribe leave law and reconcile Law911, later leave amendments and reference-date validity.

### Q26 · High · Scanned board amendment and damaged extraction

Scope: `TUC_PRI`. Indicators: `AS01;AS04;MP01;CT03;CT04`.

Law9765 amendment is scanned; Law3470 extraction is imperfect and 2023 guide is guidance.

Next action: Second-check selected manual amendment excerpts and visually reconcile suspect statute clauses with official regulations; all amendment pages received first-coder visual review.

### Q27 · High · Appraisal cessation exception and age wording

Scope: `SDE_PRI`. Indicators: `AS01;AS04;MP03`.

Article51 prints cessation without sumario for confirmed Deficiente appraisal; age wording in extraction is inconsistent.

Next action: Verify scan/official text and current safeguards before interpreting these historical clauses.

### Q28 · High · Missing complete remuneration instruments

Scope: `SDE_PRI;SJU_PRI`. Indicators: `PR03;PR04`.

Supplied career rules do not settle the full salary schedule or external additions.

Next action: Obtain reference-period pay frameworks; do not convert ranking points into monetary incentives.

### Q29 · High · External promotion framework

Scope: `ERI_PRI`. Indicators: `PR01;PR02;MP02;CT02`.

Promotion procedure depends on Law4065 and applicable calls; numeric/appraisal conditions remain unresolved.

Next action: Obtain external law and regulations; resolve promotion, training recognition and thresholds.

### Q30 · Medium · Promotion course and examination alternatives

Scope: `CHU_PRI;CHA_PRI`. Indicators: `PR01;PR02;MP02`.

Supplied routes distinguish an approved course from opposition and differ by call/post.

Next action: Check implementing calls, numeric thresholds and conditional routes; preserve distinct categories.

### Q31 · Medium · Primary scope and historic salary schedule

Scope: `JUJ_PRI`. Indicators: `CT02;PR03`.

Law2531 primary must not be replaced by secondary Law3520; recognition and updated pay need external sources.

Next action: Check primary amendments, course-point schedule and reference-date remuneration.

### Q32 · Medium · 2026 supplement and role thresholds

Scope: `SLU_PRI`. Indicators: `PR02;PR04`.

April2026 classroom addition is post/hour dependent; promotion thresholds vary by post/zone.

Next action: Check official effective period, proportionality and visually verify threshold matrix.

### Q33 · Medium · Role-specific thresholds and historic provisions

Scope: `SAL_PRI;CTE_PRI;FOR_PRI`. Indicators: `PR01;PR02;MP02`.

Experience/concept conditions and old post categories differ by route; supplied versions may be old.

Next action: Verify amendments and calls for selected comparison date; retain role-specific notes.

### Q34 · Medium · Not found is not policy absence

Scope: `all`. Indicators: `MP04;PR04`.

Search-context excerpts document reviewed sections, not an exhaustive search of provincial regulations.

Next action: Review all not_found rows after obtaining missing instruments; never recode to zero automatically.

## Working in RStudio

Open the project and run:

```r
source("R/02_load_statute_pilot.R")
View(statute_coding)
View(statute_pending)
View(statute_coverage)
```

Use `statute_coding` for case-by-indicator comparisons. `statute_full` repeats a decision for each linked evidence record and must not be counted as a decision-level table. The loader keeps its earlier filename for compatibility.

The database is saved locally in the repository. The local review page does not update the previously published Evidence Atlas, and this batch does not publish or push changes to GitHub.
