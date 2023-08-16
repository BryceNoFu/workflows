#!/usr/bin/env Rscript

# Perform edgeR's TMM method to get CPM normalized counts


# # Install packages (dplyr, BiocManager (edgeR))
# install.packages("dplyr")
# install.packages("optparse")
# install.packages("tibble")
# if (!require("BiocManager", quietly = TRUE))
#     install.packages("BiocManager")
# BiocManager::install("edgeR")
# # BiocManager::install("sva") # For batch effect removal if needed


library(edgeR)
# library(sva)
library(dplyr)
library(optparse)
library(tibble)

# Parse command line arguments
parser <- OptionParser()
parser <- add_option(parser, c("-c", "--counts"), # Counts file
                     action = "store", type = "character", default = NULL, help = "Path to counts text file")
parser <- add_option(parser, c("-m", "--meta"), # Meta file
                     action = "store", type = "character", default = NULL, help = "Path to meta text file")
parser <- add_option(parser, c("-o", "--output"), # Output file
                     action = "store", type = "character", default = NULL, help = "Path to output file") 

opt <- parse_args(parser)

# Store variables
COUNTS_FILE <- opt$counts
META_FILE <- opt$meta
OUTPUT_FILE <- opt$output

# Load counts file from featureCounts as data frame
# Remove columns 2 through 6; leave just Ensembl IDs and samples
counts.df <- read.delim(COUNTS_FILE, header = TRUE, sep = "\t", skip = 1)[, -c(2:6)]

# Load meta file as data frame
meta.df <- read.delim(META_FILE, header = TRUE, sep = "\t")

# First column (Gene IDs) as row names
counts.matrix <- data.frame(counts.df[,-1], row.names = counts.df[,1])

# Change column names for samples to be just their SRA SRR sample IDs.
# (ex: "X.data.work.SRR12345678.sam" to "SRR12345678") 
colnames(counts.matrix) <- gsub(".*?(SRR\\d+).*", "\\1", colnames(counts.matrix))
colnames(counts.matrix)

# Ryan et al's methods for EdgeR's TMM, CPM, and DEGs:
# https://bitbucket.org/lynnlab/covid-sa/src/master/RNASeq%20-%20Figure%204-6/Figure%204%20D-L.R
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8758383/

# Get dge and cpm counts
group <- factor(meta.df$condition)
dge <- DGEList(counts = as.matrix(counts.matrix), group = group)
tmm_norm <- calcNormFactors(dge, method = "TMM")
cpm_counts <- cpm(tmm_norm, log = TRUE, normalized.lib.sizes = TRUE)

head(cpm_counts)
dim(cpm_counts)

# Set genes (row names) as the first column
cpm_counts.df <- as.data.frame(cpm_counts)
cpm_counts.df <- tibble::rownames_to_column(cpm_counts.df, "GeneID")

# Write to cpm_counts.txt
write.table(cpm_counts.df, file = OUTPUT_FILE, row.names = FALSE, sep = "\t", quote = FALSE)

