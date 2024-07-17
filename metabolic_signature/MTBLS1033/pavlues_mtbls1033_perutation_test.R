rm(list=ls())

library("dplyr")
library("devtools")

setwd("/Users/yliao13/PycharmProjects/phd_class/Lab_work/data_files/MTBLS1033/POS/r_code_input/")
myTable <- read.table("input_for_r_mtbls10334.csv",header=TRUE,row.names = 1, sep = ",")

myTableTranspose <- t(myTable[, -1])

print(myTableTranspose)

factors <- myTable[ , ncol(myTable)] 

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
    {next} 
    else 
    {if(dataset[i] < 0.05){
      counts <- counts + 1
      sigIndex <- append(sigIndex, i)
      print(paste("index is:", i))
      print(paste("pvalue:", dataset[i]))
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

pvalueList_anova <- get_anova_pvalues(myTableTranspose, factors)
hist(pvalueList_anova, breaks = 100, main="pValues of variables histogram")
adjusted_pvalues_anova <- p.adjust(pvalueList_anova, method="BH")
count <- counts(adjusted_pvalues_anova)

hist(adjusted_pvalues_anova, breaks = 100, main="pValues of variables histogram")

write.csv(count[2],file="significant_index_info_5_percent.csv", row.names=F)
