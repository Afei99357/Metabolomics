rm(list=ls())

library("dplyr")
library("devtools")

setwd("/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/metabolic_signature/MTBLS1033/Urine/POS/new_analysis/R_STUDIO/")
myTable <- read.table("r_input.csv",header=TRUE,row.names = 1, sep = ",")


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
    {if(dataset[i] < 0.05){
      counts <- counts + 1
      sigIndex <- append(sigIndex, i)
    }} 
  }
  return(list(counts, sigIndex))
  # return(counts)
}

### permutation test
# for(i in 1:100){
#   pvalueList_anova <- vector()
#   factors <- sample(c(0,1), size=104, replace = TRUE)
#   pvalueList_anova <- get_anova_pvalues(myTabletTranspose, factors)
#   hist(pvalueList_anova, breaks = 100)
# 
#   adjusted_pvalues_anova <- p.adjust(pvalueList_anova, method="BH")
# 
#   count <- counts(adjusted_pvalues_anova)
#   print(count)
# }

## this is the correct target labels
factors <- unlist(tail(myTable, n =1))
data_new <- head(myTable, -1) 
pvalueList_anova <- get_anova_pvalues(data_new, factors)
hist(pvalueList_anova, breaks = 100, main="pValues of variables histogram")
adjusted_pvalues_anova <- p.adjust(pvalueList_anova, method="BH")
count <- counts(adjusted_pvalues_anova)
write.csv(count[[2]],file="pvalue_significant_index_fdr_5_percent.csv",row.names=F)

