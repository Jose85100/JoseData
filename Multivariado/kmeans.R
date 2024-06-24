F1 <- c(-2.99,3.21,1.39,0.98,-0.35,-3.54,3.02,0.14,-0.5,-1.35)
F2 <- c(1.02,0.04,-0.56,0.22,-0.5,-0.09,1.11,-0.85,-0.91,0.52)
df <-as.data.frame(cbind(F1,F2))
names(df)

c1 <- c(1,0)
c2 <- c(2,0)
centros = rbind(c1,c2)

kmedias = kmeans(df,centros)

df$cluster = kmedias$cluster
df


kmedias2 = kmeans(df,2)

############################################################
# Metodo del codo para ver con cuantas clases me quedo
set.seed(1234)
wcss <- vector()
for(i in 1:6){
  wcss[i] <- sum(kmeans(df, i)$withinss)
}

x=1:6
plot(x,wcss)

library(ggplot2)
ggplot() + geom_point(aes(x = 1:6, y = wcss), color = 'blue') + 
  geom_line(aes(x = 1:6, y = wcss), color = 'blue') + 
  ggtitle("M?todo del Codo") + 
  xlab('Cantidad de Centroides k') + 
  ylab('WCSS')

################################################
# M. WARD
matriz =dist(df)
ward = hclust(matriz,method="ward.D")
ward$height
plot(ward)
plot(ward,hang = -30,labels = FALSE)
barplot(ward$height)
