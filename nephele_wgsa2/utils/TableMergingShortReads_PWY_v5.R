# load packages
library("easypackages") # can also install multiples with packages()
x<-c("tidyverse", "reshape2", "broom", "data.table", "tibble", "docopt")
suppressMessages(libraries(x)); rm(x)

# library(docopt)
print("------> docopt settings ------")
doc <- "Usage: my_program.R [options] 
 --help              show this screen
 --pwyDIR PATH       hard path to bin dir [default: 'wdir/TEDreadsTAX/bin']
 --sfxRMV NAME       string suffix to remove from file names to obtain sampNames
 --outDIR NAME       path to & name of output directory to create [default: 'wdir/TEDreadsTAX/merged_tables']
 --genDIR PATH     hard path to bin dir for KO or EC genes [default: 'wdir/PWYprofiles/keggPWY/genebin']"
print(doc) %>% cat()

args <- docopt(doc)
print(args)
# for manual prep #this is if the .sh does not provide arguments
# args <-docopt(doc, args = c(
#  # "--wdir"  , "dbLinks/merging/table_merging_tests/ ",                             # "/path/to/WmGS_v2/tests/" ,
#  "--pwyDIR"  , "dbLinks/merging/table_merging_test/binDIR_ec/",                    # "/path/to/PWYprofiles/bin/",
#  "--sfxRMV"  ,  "_4krona.txt", 
#  "--outdir"  , "dbLinks/merging/table_merging_test/merged_tables_v5_ec/",          # "/path/to/PWYprofiles/merged_tables/" )
#  "--genDIR",  "dbLinks/merging/table_merging_test/genebin/") )
# # args
# print("-----------> docopt settings------^^^^")
# load("PWY_TableMerging_v3.RData")
# 
# #=============== finished ==============

cat("\n\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
print("------> starting PWY COLLATION <------")
input=list() 
input$files=list.files(args$pwyDIR, full.names = T, pattern = args$sfxRMV) 
names(input$files) <- basename(input$files) %>% str_remove(args$sfxRMV)
print("------> checking names of pwy input files:")
input$files

#load data from files
print("------> load data from files")
tiers=paste0(rep("Tier"), seq(1,18,1)) #assuming max(metaCyc PWY Tiers) = 18 (its actually 14)
data=list()
data=lapply(input$file, function(x){
  y<-read.table(x, header = FALSE, sep = "\t", na.strings = c("NA", "", " "), fill = TRUE,
                quote = "", check.names = FALSE, col.names = c("Counts", tiers) ) %>% remove_rownames() %>%
    group_by(across(any_of(tiers))) %>%  relocate("Counts") %>% filter(!Counts %in% "X") %>%
    unite("allTiers", any_of(tiers), sep="; ", remove=T, na.rm=T) %>%
    relocate("allTiers", .after=last_col()) %>%
    mutate(PWYname = gsub(".*; ", "", allTiers) ) %>% 
    mutate(Counts = round(as.numeric(Counts), digits = 2))
})

# lastcol <- dim(data[[1]])[[2]]; lastrow<- dim(data[[1]])[[1]]
# data[[1]][1:10, c(1:lastcol)]
# data[[1]][134:144, c(1:lastcol)]


print("------> merging PWY data")
merged0=Reduce(function(x,y) merge(x,y, by=c("allTiers","PWYname"), all=T ), data)
# head(merged0)
merged <- merged0 %>% setNames(c("allTiers", "PWYname", names(data))) %>% 
  mutate(rn = PWYname) %>% column_to_rownames("rn") %>%
  separate(allTiers, into = tiers, sep = "; ", remove = F) %>%
  discard(~all(is.na(.x))) %>%
  mutate_if(is.numeric, ~replace(. , is.na(.), 0)) %>%
  relocate("allTiers", .after=last_col())
# View(merged)

# print("------> checking merged object:")
# head(merged); tail(merged); dim(merged);

output=list()
output$dir<- args$outDIR
print(paste("------> exporting collated PWY table to:", output$dir))
dir.create(output$dir)


noHier <- setdiff(names(merged), c("allTiers"))
write.table(merged[,noHier], file.path(output$dir, "merged_Counts+PWY.txt"),
            sep="\t", col.names=NA, quote = F, na="")

noTAX <- setdiff(names(merged), tiers)
noTAX <- merged[, noTAX] %>% relocate(allTiers, .after=last_col() )
write.table(noTAX, file.path(output$dir, "merged_Counts+allTiers.txt"),
            sep="\t", col.names=TRUE, row.names = F, quote = F, na="")

# try({
# write.table(merged, file.path(output$dir, ".merged_Counts+PWY+allTiers.txt"), ## invisible file
#             sep="\t", col.names=NA, quote = F, na="")

# write.table(merged[,names(data)], file.path(output$dir, ".merged_Counts.txt"), ## invisible file
#             sep="\t", col.names=NA, quote = F, na="")

# noCounts<-setdiff(names(merged), c(names(data), "allTiers") )
# write.table(merged[,noCounts], file.path(output$dir, ".merged_PWY.txt"), ## invisible file
#             sep="\t", col.names=NA, quote = F, na="") 

# Lin <- select(merged, "allTiers")
# write.table(Lin, file.path(output$dir, ".merged_allTiers.txt"), ## invisible file
#             sep="\t", col.names=NA, quote = F, na="")
# })

# bim <-biomformat::make_biom(merged[,names(data)], observation_metadata = merged[,noCounts])
# biomformat::write_biom(bim, biom_file = paste0(output$dir, "merged_Counts+PWY_json.biom") )
# print("WARNING: please import biom with read_biom(), not with phyloseq, qiime or ampvis biom-import features")
# test biom file:
# t <-read_biom(paste0(output$dir, "merged_Counts+TAX_json.biom")) #imports
# t <- amp_import_biom(paste0(output$dir, "merged_Counts+TAX_json.biom")) #does not import
# rm(t)

##' ------------------- GENE tables merging portion -------------------------------------- '
cat("\n\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
print("------> starting GENE COLLATION <------")
if(args$genDIR == "NA" ){ print("---> no geneTABLES to merge. Disabled.")}else{
            ######## Code for merging geneTPM tables (KO and EC)
          ingenes=list()
          ingenes$files=list.files(args$genDIR, full.names = T, pattern = args$sfxRMV)##"_geneTPM.*.txt") 
          names(ingenes$files) <- basename(ingenes$files) %>% str_remove(args$sfxRMV) ##("_geneTPM.*.txt")
          print("----- checking names of gene input files:")
          print(ingenes$files)


          #load data from files
          print("------> load GENE data from gene bin")
          genedata=list()
          genedata=lapply(ingenes$files, function(x){
            y<-read.table(x, header=F, check.names = F, sep="\t", na.strings =c("NA",""," "), row.names = NULL,
                          fill=T, quote = "", col.names = c("annot", "geneTPM", "geneNAME") ) %>%
              group_by(across(any_of("annot"))) 
          })
          # names(genedata)

          print("------> merging GENE data")
          genemerged=Reduce(function(x,y)  merge(x,y, by=c("annot", "geneNAME"), all=T ), genedata)
          genemerged = genemerged %>% setNames(c("annot", "geneNAME", names(genedata)) ) %>% 
            mutate_if(is.numeric, ~replace(. , is.na(.), 0)) %>% 
            column_to_rownames("annot") %>% filter(rowSums(select_if(., is.numeric)) !=0)
          # print("------> checking genemerged object:")
          # head(genemerged); tail(genemerged); dim(genemerged);

          print(paste("------> exporting collated GENE table to:", output$dir))
          write.table(genemerged, file.path(output$dir, "merged_geneTPMtable.txt"),
                      sep="\t", col.names=NA, quote = F, na="")
 }


# rm(noCounts, noHier)
#save R image
save.image(paste0(output$dir, "/.TableMergingShortReads_v5.RData") )

