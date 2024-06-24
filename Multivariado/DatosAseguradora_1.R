setwd("E:/MATEMÁTICA/Métodos estadísticos multivariados")
library(FactoMineR)
library(readr)

library(readr)
DatosAseguradora <- read_delim("E:/MATEMÁTICA/Métodos estadísticos multivariados/DatosAseguradora.txt",delim = "\t", escape_double = FALSE, trim_ws = TRUE)
DatosAseguradora=DatosAseguradora[,-1]
attach(DatosAseguradora)
res<-MCA(DatosAseguradora, ncp = 5, ind.sup = NULL, quanti.sup = NULL, graph = TRUE,axes = c(1,2))


res$ind
barplot(res$eig[,1])
coord<-res$ind$coord

#matriz de distancia al cuadrado
matd2<-(dist(coord))^2
Ward<-hclust(matd2,method="ward.D")

#Gr??fico de los histogramas
indW <-as.vector(Ward$heigh)
length(indW)
barplot(indW)
barplot(indW[950:999])

#Corte
corte <-cutree(Ward,k=3)
cent<-NULL

for(k in 1:6){cent<-rbind(cent,colMeans(coord[corte==k,,drop=FALSE]))}

clases<-kmeans(coord,cent)
table(clases$cluster)

by(Data,clases$cluster,summary)

Data$cluster=as.factor(clases$cluster)
