# Download the assignment datasets without modifying the original files.
# Run from the educ-argentina RStudio project:
# source("R/00_download_data.R")
# Optional: select datasets before sourcing, e.g.:
# options(education.datasets = c("aprender", "relevamiento_anual"))

if (!file.exists("educ-argentina.Rproj")) {
  stop("Open educ-argentina.Rproj before running this script.")
}
manifest <- read.csv("data/download_manifest.csv", stringsAsFactors = FALSE)
selected <- getOption("education.datasets", unique(manifest$dataset))
manifest <- manifest[manifest$dataset %in% selected, , drop = FALSE]
if (!nrow(manifest)) stop("No matching datasets in the download manifest.")
old_timeout <- getOption("timeout")
options(timeout = max(1800, old_timeout))
results <- vector("list", nrow(manifest))

for (i in seq_len(nrow(manifest))) {
  destination <- manifest$relative_path[i]
  url <- manifest$url[i]
  dir.create(dirname(destination), recursive = TRUE, showWarnings = FALSE)
  status <- "already exists"
  error <- ""
  if (!file.exists(destination)) {
    temporary <- paste0(destination, ".part")
    message(sprintf("[%d/%d] %s", i, nrow(manifest), destination))
    tryCatch({
      if (startsWith(url, "https://drive.google.com/uc?")) {
        url <- sub("https://drive.google.com/uc?",
                   "https://drive.usercontent.google.com/download?", url, fixed = TRUE)
        url <- paste0(url, "&confirm=t")
      }
      code <- download.file(url, temporary, mode = "wb", method = "libcurl")
      if (code != 0 || file.info(temporary)$size == 0) stop("Download failed or empty file.")
      connection <- file(temporary, "rb")
      header <- readBin(connection, "raw", n = 256)
      close(connection)
      header_text <- paste(rawToChar(header, multiple = TRUE), collapse = "")
      if (grepl("<!doctype html|<html", header_text, ignore.case = TRUE, useBytes = TRUE)) {
        stop("Received an HTML page. Check access to the source link.")
      }
      if (!file.rename(temporary, destination)) stop("Could not save the downloaded file.")
      status <- "downloaded"
    }, error = function(e) {
      status <<- "failed"
      error <<- conditionMessage(e)
      if (file.exists(temporary)) unlink(temporary)
      message("Failed: ", error)
    })
  }
  results[[i]] <- data.frame(relative_path = destination, status = status, error = error)
}
# Extract the statutes archive after download, preserving the source folders.
statutes_zip <- "data/raw/statutes/provincial_statutes.zip"
if ("statutes" %in% selected && file.exists(statutes_zip)) {
  members <- unzip(statutes_zip, list = TRUE)$Name
  safe <- !startsWith(members, "/") & !grepl("(^|/)\\.\\.(/|$)", members)
  missing_members <- members[safe & !file.exists(file.path("data/raw/statutes", members))]
  if (length(missing_members)) {
    unzip(statutes_zip, files = missing_members, exdir = "data/raw/statutes", overwrite = FALSE)
  }
}
options(timeout = old_timeout)
results <- do.call(rbind, results)
write.csv(results, "data/last_download_run.csv", row.names = FALSE)
if (any(results$status == "failed")) {
  warning("Some downloads failed. See data/last_download_run.csv and rerun to retry.")
} else {
  message("All selected files are available in data/raw/.")
}
