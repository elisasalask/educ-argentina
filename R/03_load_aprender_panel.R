# Load the province/sector repeated-cross-section aggregates.
# From the RStudio project, first build them with scripts/build_aprender_panel.py.
# Originals remain under data/raw/aprender. No additional R packages are required.
stopifnot(file.exists('educ-argentina.Rproj'))
aggregate_dir <- 'outputs/aprender-panel-2026-11-12'
panel_path <- file.path(aggregate_dir, 'panel_provincial.csv')
if (!file.exists(panel_path)) {
  stop('Build aggregates first: python scripts/build_aprender_panel.py')
}
aprender_panel <- read.csv(panel_path, fileEncoding='UTF-8-BOM',
                          colClasses=c(provincia_codigo='character'),
                          check.names=FALSE, stringsAsFactors=FALSE)
aprender_coverage <- read.csv(file.path(aggregate_dir, 'cobertura.csv'),
                             fileEncoding='UTF-8-BOM', stringsAsFactors=FALSE)
aprender_national_2019 <- read.csv(file.path(aggregate_dir, 'muestra_nacional_2019.csv'),
                                 fileEncoding='UTF-8-BOM', stringsAsFactors=FALSE)
aprender_exceptions <- read.csv(file.path(aggregate_dir, 'sector_sin_clasificar.csv'),
                               fileEncoding='UTF-8-BOM', stringsAsFactors=FALSE)
stopifnot(!anyDuplicated(aprender_panel[c('provincia_codigo','anio','nivel','grado','sector','operativo')]))
message(nrow(aprender_panel), ' province-sector rows loaded with original score-variable names. See the output methods before comparing editions.')
# Example: View(subset(aprender_panel, nivel == 'Primaria' & grado == '6.º grado', select=c(provincia, anio, sector, lpuntaje, mpuntaje)))
