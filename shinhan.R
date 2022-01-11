library(dplyr)
library(ggplot2)
library(caret)
library(NbClust)
# 외국인 데이터
card_foreigner <- read.table(file = "data/FOREIGNER.txt", header = TRUE, sep = "|", encoding =  "UTF-8")
head(card_foreigner)
colnames(card_foreigner)
# 내국인 데이터 
card_native <- read.table(file = "data/NATIVE.txt", header = TRUE, sep = "|", encoding =  "UTF-8")
head(card_native)

# 예방 접종 데이터
covid19_vaccine <- read.table(file = "covid19_vaccine_(210704).csv", header = TRUE)
head(covid19_vaccine)
card_native = native%>%filter(ta_ym>202000 & v1!=v2)%>%select(v1,v2)
# K-means clustering test
set.seed(1000)
trainingRowIndex = sample(1:nrow(card_foreigner), 0.7*nrow(card_foreigner))
trainingData = card_foreigner[trainingRowIndex,]
testData = card_foreigner[-trainingRowIndex,]
trainingData
testData
# normalization
trainingData.normal <- scale(trainingData[-5])
summary(trainingData.normal)
# model
card_foreigner.kmeans <- kmeans(trainingData.normal[,-5], centers = 3, iter.max = 10000)
card_foreigner.kmeans$centers
# k-means 군집
trainingData$cluster <- as.factor(card_foreigner.kmeans$cluster)
qplot(Petal.Width, Petal.length, colour = cluster, data = trainingData)

