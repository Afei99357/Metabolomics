rm(list=ls())

library("dplyr")
library("devtools")

setwd("/Users/ericliao/Downloads/")
myTable <- read.table("st000058_group7.csv",header=TRUE,row.names = 1, sep = ",")

myTabletTranspose <- t(myTable)

get_anova_pvalues <- function(dataframe, factors) {
  pvalueList <- vector()
  for(i in 1: nrow(dataframe)){
    pvalueList[i] <- anova(lm(factors ~ as.numeric(dataframe[i,])))$"Pr(>F)"[1]
  }
  return(pvalueList)
}

counts <- function(dataset) {
  sigIndex <- vector()
  counts <- 0
  for(i in 1: length(dataset)){
    
    if(is.na(dataset[i])) 
    {print(i)} 
    else 
    {if(dataset[i] < 0.15){
      counts <- counts + 1
      sigIndex <- append(sigIndex, i)
    }} 
  }
  return(list(counts, sigIndex))
  # return(counts)
}

### permutation test
# for(i in 1:50){
#   pvalueList_anova <- vector()
#   factors <- sample(c(0,1), size=8, replace = TRUE)
#   pvalueList_anova <- get_anova_pvalues(myTabletTranspose, factors)
#   hist(pvalueList_anova, breaks = 100)
# 
#   adjusted_pvalues_anova <- p.adjust(pvalueList_anova, method="BH")
# 
#   count <- counts(adjusted_pvalues_anova)
#   print(count)
# }

## this is the correct target labels
factors <- c(1, 1, 0, 0, 0, 1, 1, 0)
pvalueList_anova <- get_anova_pvalues(myTabletTranspose, factors)
hist(pvalueList_anova, breaks = 100, main="pValues of variables histogram")
adjusted_pvalues_anova <- p.adjust(pvalueList_anova, method="BH")
count <- counts(adjusted_pvalues_anova)


