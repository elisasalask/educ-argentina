# Data sources and initial download scope

Sources were taken from hyperlinks in `API-209 Final Exercise - 2026 - fv.docx`, Appendix 2, and the provincial statute link in the assignment text. Files were retrieved on 2026-11-04. Raw files are stored locally and excluded from Git uploads.

| Source | Selected files | Course or official source |
| --- | --- | --- |
| Aprender | All supplied CSVs for 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025 | https://drive.google.com/drive/folders/16_lO7KbhwwD458YeciPYVh8RF9ttYywW |
| Relevamiento Anual | Seven supplied CSVs per folder, 2011–2025 | https://drive.google.com/drive/folders/1DHVXpX8BNsr0TgpYFFfrV6O4q9OklIi8 |
| ERCE 2019 | Nine Stata files, nine questionnaires, and manual | https://drive.google.com/drive/folders/1BmfThpO7HmrxzehucMqNqwEp3wShcmin |
| PISA | Core 2022 student, school, and teacher Stata files; six Argentina questionnaires | https://drive.google.com/drive/folders/1LrYyzMzupw2t9k03ERgECJdmAa_UCfBp |
| Teacher salaries | Five Excel series linked from the official CGECSE page | https://www.argentina.gob.ar/capital-humano/educacion/informacion-y-evaluacion-educativa/series-salario-docente |
| Provincial statutes | Course Dropbox archive, extracted under `data/raw/statutes/` | https://www.dropbox.com/scl/fo/q5u2smz5v8krbmfxjkylk/ANJLiNSHkuqa8ic9VcPZHW4?rlkey=r9b6t189ypg4m9venzwk2h00j&dl=1 |

## Source issues and boundaries

- The RA 2019 folder contains `RA_2018_Matricula.csv` and `RA_2018_Trayectoria.csv`. These names are preserved. Confirm the actual reference year before treating these as 2019 observations.
- PISA's folder called `Argentina` contains questionnaires, not Argentina-only microdata. The selected core 2022 Stata files are international files; select Argentina using the country identifier after checking labels. The teacher file does not establish that Argentina participated in the teacher questionnaire.
- PISA historical cycles, duplicate formats, timing/cognitive files, and precomputed instructor outputs are not downloaded by default. Their discovered source links are in `data/course_file_inventory.csv`.
- Aprender Stata copies of three student files are omitted because CSV originals are already selected. The unrelated notebook is omitted.
- Check actual coverage and availability of teacher questionnaires for each Aprender edition. Do not infer coverage from the year folder alone.
- Salary filenames do not identify the complete reference period. Check workbook sheets and notes for dates, seniority, workload, currency, and the definition of each salary measure before comparing provinces or years.
- Keep all sources' original labels. Statutes describe formal rules; these datasets describe conditions and outcomes. Cross-source records are not consistently linkable and do not by themselves support causal claims.

- The course statutes archive contains 23 jurisdiction folders; Misiones is missing. The 51 documents include statutes and related regulations. Obtain the missing Misiones statute before claiming coverage of all 24 jurisdictions.

- `ERCE_2019_QA6.dta` requires `haven::read_dta(path, encoding = "latin1")` in the R installation used for verification. Default encoding produced an invalid byte sequence error; the Latin-1 setting opened the file successfully.

## Reproducibility

`data/download_manifest.csv` records each selected download URL. `data/download_status.csv` records the initial retrieval status and SHA-256 checksum of each successfully downloaded selected file. The inventory records source links, not permission to republish instructor-provided data. Share code and download instructions with the team.

All 171 selected downloads completed. Basic checks opened a sample row from each CSV and Stata file, read the five Excel workbooks, verified PDF signatures, and listed the statutes ZIP. These checks establish basic readability, not substantive data validity. Results are in `data/file_validation.csv`.
