data(wine)
windows()
windows()
res <- MFA(wine, group=c(2,3,4,5,6,7,8,9,10,11,12,13), type=c("n",rep("s",5)),
           ncp=5)

summary(res)
barplot(res$eig[,1],main="Eigenvalues",names.arg=1:nrow(res$eig))
