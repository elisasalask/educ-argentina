# Load and validate the statute coding pilot from the RStudio project root.
# Tables are UTF-8 and require no extra R packages.
if (!file.exists('educ-argentina.Rproj')) stop('Open the educ-argentina RStudio project first.')
pilot_dir <- 'data/statute_coding'
read_pilot <- function(name) read.csv(file.path(pilot_dir,name),stringsAsFactors=FALSE,fileEncoding='UTF-8',check.names=FALSE)
statute_codebook <- read_pilot('codebook_v0_1.csv')
statute_coding <- read_pilot('pilot_coding.csv')
statute_evidence <- read_pilot('pilot_evidence.csv')
statute_documents <- read_pilot('pilot_documents.csv')
stopifnot(!anyDuplicated(statute_coding$row_id), !anyDuplicated(statute_evidence$evidence_id),
          !anyDuplicated(statute_documents$document_id),
          all(statute_coding$indicator_id %in% statute_codebook$indicator_id),
          all(statute_evidence$row_id %in% statute_coding$row_id),
          all(statute_evidence$document_id %in% statute_documents$document_id),
          all(table(statute_coding$case_id) == nrow(statute_codebook)))
# Source downloads retain an archive folder-placement error for Misiones.
# Resolve it for review without changing the original archive or other documents.
statute_documents$resolved_source_file <- statute_documents$source_file
mis <- statute_documents$document_id == 'MIS1'
if (any(mis) && !file.exists(statute_documents$source_file[mis])) {
  original <- sub('/Misiones/','/Mendoza/',statute_documents$source_file[mis],fixed=TRUE)
  if (file.exists(original)) statute_documents$resolved_source_file[mis] <- original
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
# subset(statute_pilot_full, indicator_id == 'CT04' & case_id != 'COR_SEC')
# In RStudio's Console: View(statute_coding), View(statute_evidence)
