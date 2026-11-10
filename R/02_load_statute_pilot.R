# Load and validate the unified statute coding database from the RStudio project root.
# Tables are UTF-8 and require no extra R packages.
if (!file.exists('educ-argentina.Rproj')) stop('Open the educ-argentina RStudio project first.')
pilot_dir <- 'data/statute_coding'
read_pilot <- function(name) read.csv(file.path(pilot_dir,name),stringsAsFactors=FALSE,fileEncoding='UTF-8',check.names=FALSE)
statute_codebook <- read_pilot('codebook.csv')
statute_coding <- read_pilot('statute_coding.csv')
statute_evidence <- read_pilot('statute_evidence.csv')
statute_documents <- read_pilot('statute_documents.csv')
statute_pending <- read_pilot('pending_decisions.csv')
statute_coverage <- read_pilot('jurisdiction_coverage.csv')
statute_review_queue <- read_pilot('review_queue.csv')
stopifnot(!anyDuplicated(statute_coding$row_id), !anyDuplicated(statute_evidence$evidence_id),
          !anyDuplicated(statute_documents$document_id),
          all(statute_coding$indicator_id %in% statute_codebook$indicator_id),
          all(statute_evidence$row_id %in% statute_coding$row_id),
          all(statute_evidence$document_id %in% statute_documents$document_id),
          all(table(statute_coding$case_id) == nrow(statute_codebook)))
# Resolve canonical names or original archive aliases without modifying sources.
statute_documents$resolved_source_file <- statute_documents$source_file
for (i in seq_len(nrow(statute_documents))) {
  if (!file.exists(statute_documents$source_file[i]) &&
      nzchar(statute_documents$archive_source_file[i]) &&
      file.exists(statute_documents$archive_source_file[i])) {
    statute_documents$resolved_source_file[i] <- statute_documents$archive_source_file[i]
  }
}
missing_sources <- statute_documents$source_file[!file.exists(statute_documents$resolved_source_file)]
if(length(missing_sources)) warning('Some local source PDFs are missing. Run the download script and inspect statute_documents.')
statute_pilot_full <- merge(statute_coding,statute_evidence,by='row_id',all.x=TRUE,sort=FALSE)
statute_pilot_full <- merge(statute_pilot_full,statute_documents,by='document_id',all.x=TRUE,sort=FALSE,
                           suffixes=c('','_document'))
message(nrow(statute_coding),' coding decisions; ',nrow(statute_evidence),' evidence excerpts; ',
        length(unique(statute_coding$province)),' provinces; ',length(unique(statute_coding$case_id)), ' comparison cases.')
print(with(statute_coding,table(case_id,provision_status)))
# Example: inspect primary substitute provisions and linked evidence.
# subset(statute_coding, indicator_id == 'CT04' & grepl('_PRI$', case_id))
# Primary national-reference cases still need their applicability caveats respected.
# In RStudio's Console: View(statute_coding), View(statute_evidence)

# Current unified evidence join; older name retained for existing notebooks.
statute_full <- statute_pilot_full
