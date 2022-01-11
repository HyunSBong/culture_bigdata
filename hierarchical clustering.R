#인코딩 문제 해결 위해 read.any 함수 생성
library(readr)

read.any <- function(text, sep = "", ...) {
  
  encoding <- as.character(guess_encoding(text)[1,1])
  setting <- as.character(tools::file_ext(text))
  if(sep != "" | !(setting  %in% c("csv", "txt")) ) setting <- "custom"
  separate <- list(csv = ",", txt = "\n", custom = sep)
  result <- read.table(text, sep = separate[[setting]], fileEncoding = encoding, ...)
  return(result)
  
}

library(dplyr)
library(readxl)
df_vaccine = read.any("0704인구수대비접종률데이터.csv", header=T)
df_vaccine = df_vaccine[, c(3, 4)]
df_vaccine

library(factoextra)

#normalizing
normalize <- function(x){
  return((x-min(x)) / (max(x) - min(x)))
}
df_vaccine$총인구수 = normalize(df_vaccine$총인구수)
df_vaccine


#유입인원과 확진자수의 상관관계 파악
corona = read.any("0704인구수대비코로나감염률데이터.csv", header = T)
corona = corona %>% select(-X) %>% filter(!(행정기관 == '전국'))
corona

v2_group = read.any("df_immunisation - df_immunisation.csv", header=T)
nw = v2_group %>% select(-X) %>% group_by(유입대상지역) %>% summarise(sum(유입인구))
colnames(nw) = c("행정기관", "유입인구")
nw

#newData = 행정기관, 감염자수, 총인구수, 감염률, 유입인구
newData = merge(corona, nw)
newData

cor.test(newData$"감염률", newData$"유입인구")
#p-value = 0.144, cor = 0.3697855이므로 관련 없음


# 화장실 데이터 가져오기
toilet = read.any("시도별공공화장실수.csv", header = T)
toilet = toilet %>% select(-X)

유동인구 = read.any("df_total_immunisation - df_total_immunisation.csv", header=T)
유동인구 = 유동인구[,-c(1,3)]
names(유동인구)[1] = "행정기관"
toilet = left_join(toilet, 유동인구, by="행정기관")
toilet$화장실비율 = toilet$화장실수/toilet$유동인구

toilet = toilet[,-c(2,3)]


immun = read.any("df_total_immunisation.csv", header = T)
immun
nw = immun %>% select(-X)
nw
colnames(nw) = c("행정기관", "접종률")

#newData = 행정기관, 감염자수, 총인구수, 감염률, 유입인구, 화장실비율
newData = merge(newData, toilet)
newData

#newData = 행정기관, 감염자수, 총인구수, 감염률, 유입인구, 화장실비율, 접종률
newData = merge(newData, nw)
newData

#clustering 위한 열 선별 및 정규화
new = newData %>% select(감염률, 화장실비율, 접종률)
new$화장실비율 = as.numeric(new$화장실비율)
new
new$화장실비율 = normalize(new$화장실비율)
new

#clustering
library(ClusterR)
library(cluster)

km = kmeans(new, 3)
plot(new, col = km$cluster)


#clustering plot
library(ClusterR)
library(cluster)

##아래 결과가이상함

########################################

library(factoextra)

new1 = new[,-1] #화장실수 & 접종률
new1
new2 = new[,-2] #감염률 & 접종률
new2
new3 = new[,-3] #화장실수 & 접종률
new3

km = kmeans(new1, 4)
fviz_cluster(km,data=new1,stand=F)
plot(new1, col = km$cluster)

km = kmeans(new2, 4)
fviz_cluster(km,data=new2,stand=F)
plot(new2, col = km$cluster)

km = kmeans(new3, 4)
fviz_cluster(km,data=new3,stand=F)
plot(new3, col = km$cluster)

#######################################

#test
km = kmeans(new, 3)
fviz_cluster(km,data=new,stand=T)

#######################################

#안전한 지역
dat = newData %>% select(행정기관, 감염률, 화장실비율, 접종률)
dat = dat %>% filter(new$감염률 < mean(new$감염률) & new$화장실비율> mean(new$화장실비율) & new$접종률 > mean(new$접종률))
dat

#######################################


y_kmeans = km$cluster
clusplot(new[, c("감염률", "화장실비율")],
         y_kmeans,
         lines = 0,
         shade = TRUE,
         color = TRUE,
         labels = 2,
         plotchar = FALSE,
         span = TRUE,
         main = paste("Cluster km"),
         xlab = '감염률',
         ylab = '화장실수')

clusplot(new[, c("감염률", "접종률")],
         y_kmeans,
         lines = 0,
         shade = TRUE,
         color = TRUE,
         labels = 2,
         plotchar = FALSE,
         span = TRUE,
         main = paste("Cluster km"),
         xlab = '감염률',
         ylab = '접종률')

clusplot(new[, c("화장실수", "접종률")],
         y_kmeans,
         lines = 0,
         shade = TRUE,
         color = TRUE,
         labels = 2,
         plotchar = FALSE,
         span = TRUE,
         main = paste("Cluster km"),
         xlab = '화장실수',
         ylab = '접종률')

new[, c("감염률", "화장실수")]
y_kmeans





##########################################
##########################################
#밀도 기반 클러스터링 (???) !!!!!!!!!!!! 여기 실행하지 마세요 !!!!!!!!!!

##-- DBSCAN using fpc or dbscan package
install.packages("fpc")
library(fpc)


## Compute DBSCAN using fpc package
set.seed(17)
db <- fpc::dbscan(new2, eps = 0.004, MinPts = 5) #Eps(Epsilon): 반경 / MinPts: Eps 내 최소 점의 개수 기준
#library("factoextra")
fviz_cluster(db, new2, stand = FALSE, frame = FALSE, geom = "point")


#eps, minpts 값 찾기
install.packages('dbscan')
library(dbscan)

dbscan::kNNdistplot(new2, k=4)
abline(h = 0.15, lty = 2)


###########################################
###########################################
#계층적 군집 분석

#new1 화장실수 & 접종률
dist_new <- dist(scale(new1), method = "euclidean") #거리 계산
new.hclust <- hclust(dist_new, method = "ward.D") #군집분석
summary(new.hclust) #계층적 군집분석
plot(new.hclust)

#new2 감염률 & 접종률
dist_new <- dist(scale(new2), method = "euclidean") #거리 계산
new.hclust <- hclust(dist_new, method = "ward.D") #군집분석
summary(new.hclust) #계층적 군집분석
plot(new.hclust)

#new3 화장실수 & 접종률
dist_new <- dist(scale(new3), method = "euclidean") #거리 계산
new.hclust <- hclust(dist_new, method = "ward.D") #군집분석
summary(new.hclust) #계층적 군집분석
plot(new.hclust)


#new 전체
dist_new <- dist(scale(new), method = "euclidean") #거리 계산
new.hclust <- hclust(dist_new, method = "ward.D") #군집분석
summary(new.hclust) #계층적 군집분석
plot(new.hclust)

cutree_new_avg <- cutree(new.hclust, k=3)
table(cutree_new_avg)
table(substring(names(cutree_new_avg),1,str_locate(names(cutree_new_avg), "_")[1,1]-1),cutree_new_avg)





# 계층적 군집 분석 2
#new1 화장실수 & 접종률
library(NbClust)
dist_new <- dist(scale(new1), method = "euclidean") #거리 계산
new.hclust <- hclust(dist_new, method = "ward.D") #군집분석
summary(new.hclust) #계층적 군집분석
plot(new.hclust, hang=-1, cex=0.8)
nc <- NbClust(new1, distance = "euclidean", min.nc = 2, max.nc = 15, method = "ward.D")
rect.hclust(new.hclust, k=3, border = "red")

#new2 감염률 & 접종률
dist_new <- dist(scale(new2), method = "euclidean") #거리 계산
new.hclust <- hclust(dist_new, method = "ward.D") #군집분석
summary(new.hclust) #계층적 군집분석
plot(new.hclust, hang=-1, cex=0.8)
nc <- NbClust(new1, distance = "euclidean", min.nc = 2, max.nc = 15, method = "ward.D")

#new3 화장실수 & 접종률
dist_new <- dist(scale(new3), method = "euclidean") #거리 계산
new.hclust <- hclust(dist_new, method = "ward.D") #군집분석
summary(new.hclust) #계층적 군집분석
plot(new.hclust, hang=-1, cex=0.8)
nc <- NbClust(new1, distance = "euclidean", min.nc = 2, max.nc = 15, method = "ward.D")


#new 전체
dist_new <- dist(scale(new), method = "euclidean") #거리 계산
new.hclust <- hclust(dist_new, method = "ward.D") #군집분석
summary(new.hclust) #계층적 군집분석
plot(new.hclust, hang=-1, cex=0.8)

cutree_new_avg <- cutree(new.hclust, k=3)
table(cutree_new_avg)
table(substring(names(cutree_new_avg),1,str_locate(names(cutree_new_avg), "_")[1,1]-1),cutree_new_avg)
