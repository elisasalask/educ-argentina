# Rebuild the aggregate data used by the teaching-careers context website.
# Run from the educ-argentina RStudio project. Requires readxl and jsonlite.
stopifnot(file.exists('educ-argentina.Rproj'))
output <- '../teaching-careers-context/dist'
dir.create(output, recursive=TRUE, showWarnings=FALSE)
ra <- read.csv2('data/raw/relevamiento_anual/2023/RA_2023_Matricula.csv', check.names=FALSE, colClasses=c(ID='character'))
stopifnot(!anyDuplicated(ra$ID))
ra <- ra[ra$primaria6 == 'X' | ra$primaria7 == 'X', ]
# Count primary grades only. Grade 7 belongs to primary only in the 7-year structure.
grade_columns <- paste0('_',1:6)
ra$enrollment <- rowSums(ra[,grade_columns],na.rm=TRUE) + ifelse(ra$primaria7=='X',ifelse(is.na(ra$`_7`),0,ra$`_7`),0)
ra$missing_all_grades <- rowSums(!is.na(ra[,grade_columns])) == 0
# Aggregate only: no school IDs or individual records go to the website.
split_ra <- split(ra,list(ra$provincia,ra$sector,ra$ambito),drop=TRUE)
schools <- do.call(rbind,lapply(split_ra,function(x) data.frame(province=x$provincia[1],sector=x$sector[1],area=x$ambito[1],schools=nrow(x),enrollment=sum(x$enrollment),missing_all_grades=sum(x$missing_all_grades))))
read_salary <- function(path,measure){
 x <- readxl::read_excel(path,col_names=FALSE,.name_repair='minimal')
 # Locate the first table by its row labels; its first 24 jurisdiction rows follow row 6.
 stopifnot(grepl('Jurisdicci',x[[1]][5]))
 names <- trimws(gsub(' *\\([0-9]+\\)','',as.character(x[[1]][7:30])))
 year <- NA_integer_; pieces <- list()
 for(j in 2:ncol(x)) {
  if(!is.na(x[[j]][5])) year <- suppressWarnings(as.integer(x[[j]][5]))
  month <- as.character(x[[j]][6])
  if(is.na(year) || is.na(month) || !year %in% 2023:2026) next
  values <- suppressWarnings(as.numeric(x[[j]][7:30]))
  pieces[[length(pieces)+1]] <- data.frame(province=names,year=year,month=month,measure=measure,value=values)
 }
 do.call(rbind,pieces)
}
salaries <- rbind(read_salary('data/raw/teacher_salaries/1._salario_bruto_mg10.xlsx','gross'),read_salary('data/raw/teacher_salaries/2._salario_de_bolsillo_mg10_1.xlsx','takehome'))
stopifnot(length(unique(salaries$province))==24,all(unique(salaries$province) %in% unique(ra$provincia)))
teachers <- read.csv2('data/raw/aprender/2023/Aprender_2023_Docente_6grado_Primaria_Censal.csv',colClasses=c(ID='character'))
obj <- list(schools=schools,salaries=salaries,meta=list(ra_year=2023,primary_records=nrow(ra),teacher_questionnaire_records=nrow(teachers),teacher_questionnaire_school_ids=length(unique(teachers$ID)),all_missing_primary_grade_records=sum(ra$missing_all_grades),generated='2026-11-05',salary_position='Primary classroom teacher, single shift, 10 years of seniority'))
json <- jsonlite::toJSON(obj,auto_unbox=TRUE,na='null',digits=8)
writeLines(paste0('window.CONTEXT_DATA = ',json,';'),file.path(output,'data.js'))
write.csv(schools,file.path(output,'ra_primary_2023.csv'),row.names=FALSE)
write.csv(salaries,file.path(output,'salary_comparison.csv'),row.names=FALSE)
cat('Primary records:',nrow(ra),'enrollment:',sum(ra$enrollment),'all missing grades:',sum(ra$missing_all_grades),'\n')
