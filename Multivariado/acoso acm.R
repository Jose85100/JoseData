setwd("D:/MATEMÁTICA/Métodos estadísticos multivariados")
library(FactoMineR)
library(ade4)

acosr <- read.table("acoso.txt", header = TRUE,row.names=1,stringsAsFactors=T)


# lectura de datos
violencia <- acosr[,1:30]
acoso <- acosr[,31:50]


#ACM1
windows()
acm1=MCA(violencia, ncp = 5, ind.sup = NULL, quanti.sup = NULL, 
        quali.sup =c(23,24,25,26,27), graph = TRUE, axes = c(1,2), row.w = NULL)
windows()
barplot(acm1$eig[,1])

plot(acm1)

#ACM 2
windows()
acm2=MCA(acoso, ncp = 5, ind.sup = NULL, quanti.sup = NULL, 
        quali.sup =c(31,32,33,34,35 ), graph = TRUE, axes = c(1,2), row.w = NULL)

windows()
barplot(acm2$eig[,1])

plot(acm2)
