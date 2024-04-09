#!/usr/bin/env Rscript

install.packages(c("broom", "tibble", "docopt", "reshape2", "data.table", "biomformat", "fossil", "ggplot2", "vegan", "remotes", "BiocManager", "foreach"), repos="http://cran.us.r-project.org")
BiocManager::install("biomformat")
remotes::install_github("kasperskytte/ampvis2")
BiocManager::install("S4Vectors")
install.packages("easypackages", repos="http://cran.us.r-project.org")
install.packages("tidyverse", repos="http://cran.us.r-project.org")