library(FactoMineR)
library(readxl)
library("factoextra")
#install.packages(c("FactoMineR","readxl","factoextra"))

setwd("D:/INVESTIGACIÓN")

Empresa_cualit <- read_excel("D:/INVESTIGACIÓN/Empresa_cualit.xlsx")
Empresa <- read_excel("D:/INVESTIGACIÓN/Empresa.xlsx")

types <- sapply(General, typeof)
print(types)

#################################################################################################################################################
#Análisis Factorial Múltiple de las empresas
Mulfactor<-MFA (Empresa, group=c(8,3), type = c("n","s"), ncp = 5, name.group = NULL, graph = TRUE,row.w = NULL, axes = c(2,3), tab.comp=NULL)

eig.val <- get_eigenvalue(Mulfactor)
head(eig.val,40)
fviz_screeplot(Mulfactor)

##Grupo de variables
group <- get_mfa_var(Mulfactor, "group")
group

# Coordinates of groups
head(group$coord)
# Cos2: quality of representation on the factore map
head(group$cos2)
# Contributions to the  dimensions
head(group$contrib)


fviz_mfa_var(Mulfactor, "group")

# Contribution to the first dimension
fviz_contrib(Mulfactor, "group", axes = 1)
# Contribution to the second dimension
fviz_contrib(Mulfactor, "group", axes = 2)
# Contribution to the second dimension
fviz_contrib(Mulfactor, "group", axes = 3)

#VARIABLES CUANTITATIVAS
quanti.var <- get_mfa_var(Mulfactor, "quanti.var")
quanti.var
 
# Coordinates
head(quanti.var$coord)
# Cos2: quality on the factore map
head(quanti.var$cos2)
# Contributions to the dimensions
head(quanti.var$contrib)

fviz_mfa_var(res.mfa, "quanti.var", palette = "jco", 
             col.var.sup = "violet", repel = TRUE)

fviz_mfa_var(res.mfa, "quanti.var", palette = "jco", 
             col.var.sup = "violet", repel = TRUE,
             geom = c("point", "text"), legend = "bottom")
# Contributions to dimension 1
fviz_contrib(res.mfa, choice = "quanti.var", axes = 1, top = 20,
             palette = "jco")

# Contributions to dimension 2
fviz_contrib(res.mfa, choice = "quanti.var", axes = 2, top = 20,
             palette = "jco")

fviz_mfa_var(res.mfa, "quanti.var", col.var = "contrib", 
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"), 
             col.var.sup = "violet", repel = TRUE,
             geom = c("point", "text"))

fviz_mfa_ind(res.mfa, 
             habillage = "Label", # color by groups 
             palette = c("#00AFBB", "#E7B800", "#FC4E07"),
             addEllipses = TRUE, ellipse.type = "confidence", 
             repel = TRUE # Avoid text overlapping
             ) 

fviz_ellipses(res.mfa, c("Label", "Soil"), repel = TRUE)
fviz_mfa_ind(res.mfa, partial = "all") 

fviz_mfa_axes(res.mfa)

#################################################################################################################################################
#https://rpubs.com/ocamilocardona/813536
library(FactoMineR)
library(ggplot2)
library(FactoClass)
library(factoextra)
library(Rcpp)
library(broom)
library(pander)
library(corrplot)
library(gridExtra)


Mulcorres <- MCA(Empresa_cualit, ncp = 5, ind.sup = NULL, quanti.sup = NULL,
    quali.sup = NULL, excl=NULL, graph = TRUE,
    level.ventil = 0, axes = c(1,2), row.w = NULL,
    method="Indicator", na.method="NA", tab.disj=NULL)


F1<-ggplot(Datos, aes(x=Carrera)) + geom_bar(fill= "#DDB4EB")
F2<-ggplot(Datos, aes(x=Sexo)) + geom_bar(fill= "#FFD4A5")
F3<-ggplot(Datos, aes(x=Estrato)) + geom_bar(fill= "#41894A")
F4<-ggplot(Datos, aes(x=Origen)) + geom_bar(fill= "#FFEC28")
F5 <- grid.arrange(F1,F2,F3,F4, nrow = 2)

eigenval <- get_eigenvalue(uni.mca)
pander(head(eigenval))

fviz_screeplot(uni.mca, addlabels = TRUE, ylim = c(0, 15)) + geom_hline(yintercept = 7.14, linetype = 2, color = "red")

fviz_mca_biplot(uni.mca, repel = TRUE, 
                ggtheme = theme_grey())+labs(
                  title ="           Representación simultanea de los individuos y las categorías")

var <- get_mca_var(uni.mca)
var

fviz_mca_var(uni.mca, choice = "mca.cor",
             repel = TRUE,
             ggtheme = theme_grey())


pander(head(var$cos2, 15))

fviz_mca_var(uni.mca, col.var = "purple", shape.var = 10, repel = TRUE,
             ggtheme = theme_grey())+labs(title = "                     Nube de puntos de las Modalidades/Categorías")


fviz_cos2(uni.mca, choice = "var", axes = 1:2)+labs(title = "Cos2 de Categorías para las Dimensiones 1-2")


corrplot(var$cos2, is.corr = FALSE)

pander(head(round(var$contrib,2), 15))

fviz_contrib(uni.mca, choice = "var", axes = 1, top = 15)+labs(title = "Contribución de las Categorías para las Dimensión 1")

fviz_contrib(uni.mca, choice = "var", axes = 2, top = 15)+labs(title = "Contribución de las Categorías para las Dimensión 2")

fviz_contrib(uni.mca, choice = "var", axes = 1:2, top = 15)+labs(title = "Contribuciones de las Categorías para las Dimensiónes 1-2")

fviz_mca_var(uni.mca, col.var = "contrib", 
             gradient.cols = c("#00AFBB", "#E7B800","#FC4E07"),
                ggtheme = theme_grey()
             , repel = TRUE)

est <- get_mca_ind(uni.mca)
est

pander(head(est$coord))
pander(head(est$cos2))
pander(head(est$contrib))

fviz_mca_ind(uni.mca, col.ind = "cos2",
             gradient.cols= c("blue", "white", "red"),
             repel = TRUE,
             ggtheme = theme_grey())

tail(est$contrib)

fviz_cos2 (uni.mca, choice = "ind", axes = 1:2, top = 50)+labs(title = "Cos2 de los individuos para las Dimensiónes 1-2")

fviz_mca_ind(uni.mca,
            label = "none",
            habillage = Sexo,
            pallette = c("#CCCCFF", "#F08080"),
            addEllipses = TRUE,
            ggtheme = theme_grey())

fviz_ellipses(uni.mca, 1:4, 
              geom = "point")

uni.desc <- dimdesc(uni.mca, axes = c(1,2))

#Prueba de hipotesis:

#H0: La variable o clasificacion no es caracteristica en la dimension
#H1: La variable o clasificacion es caracteristica en la dimensión


#Descripcion de la primera dimensión

uni.desc[[1]]
uni.desc[[2]]

sup.mca<- MCA(NuevosDatos,quali.sup = 5,ncp=2,graph = FALSE)
coor_cat<- sup.mca$quali.sup$coord
pander(coor_cat)

fviz_mca_var(sup.mca,repel=T)+labs(
  title ="                     Nube de puntos de Categorias y Edad Suplementaria")

#################################################################################################################################################

