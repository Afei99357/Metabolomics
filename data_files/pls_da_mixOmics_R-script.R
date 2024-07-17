if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")

BiocManager::install("mixOmics", forc=TRUE)

# loading library
library(MASS)
library(lattice)
library(ggplot2)
library(mixOmics)

# loading data
lipids <- read.csv("/Users/yliao13/Downloads/LipidsWG_QEHF_POS_processed_with_mz_preprocessing.csv", row.names = 1, header=TRUE)

lipids_data <- lipids[,-1]

lipids_data

X <- lipids_data[c(1:15),]

## target 2 groups
#Y <- c(0,0,0,0,0,0,0,0,0,1,1,1,1,1,1)

Y <-lipids$target

Y

aplsda <- plsda(X, Y)

plotIndiv(plsda)

## create dummy matrix according to the classes
Y.mat <-unmap(Y)

# pls regression
res <- pls(X, Y.mat,ncomp = 2)

res
val <- perf(res, criterion = c("R2",'Q2'),validation="loo")
val

val$measures$Q2
