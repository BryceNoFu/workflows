source('http://bioconductor.org/biocLite.R')
biocLite("withr")
biocLite("rstudioapi")
biocLite("devtools")
biocLite("pachterlab/sleuth")

install.packages("dplyr")
install.packages("tidyverse")
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
# BiocManager::install(version = "3.16")
BiocManager::install('locfit')
BiocManager::install("EnhancedVolcano", dependencies = T)
BiocManager::install("DESeq2", dependencies = T)
BiocManager::install("biomaRt")
BiocManager::install("gplots")


# In the case EnhancedVolcano fails to install using BiocManager, pull the package off of github
if (!require("EnhancedVolcano", quietly = TRUE))
    devtools::install_github('kevinblighe/EnhancedVolcano')

install.packages("readxl")
install.packages("tibble")