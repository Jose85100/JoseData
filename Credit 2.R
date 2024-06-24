#################################################################################
# Cargar bibliotecas necesarias
library(FactoMineR)
library(cluster)
library(readxl)

#################################################################################
setwd("D:/MATEMÁTICA/Métodos estadísticos multivariados")

Credit <- read.csv("Credit.csv", header = TRUE)

Credit_1 <- Credit[, !(names(Credit) %in% c("Variable.continuous.1", "Variable.continuous.2"))]

#################################################################################
# Crear la variable "group" como un factor a partir de la variable "Type.of.client"
Data_mfa <- Credit_1
Data_mfa <- Data_mfa[, c("Seniority","Mean.of.mouvements","Cumulative.debits","Age.of.client", "Family.Situation","Profession","Home.of.employee","Size.of.savings","Active.mean","Type.of.client","Checkbook.not.allowed","overdraft.authorized")]

# Ejecutar el an??lisis MFA
res.mfa <- MFA(Data_mfa, group = c(3, 3, 3, 3), type = c(rep("n", 4)), ind.sup = NULL, name.group = c("Transaccional", "Personal", "Ingresos/Riqueza", "RelaciÃ³n banco"), num.group.sup = NULL, graph = TRUE)

# Obtener los resultados del analisis MFA
summary(res.mfa)

#################################################################################
# Crear la variable "group" como un factor a partir de la variable "Type.of.client"
Data_mfa1 <- Credit_1
Data_mfa1 <- Data_mfa1[, c("Type.of.client","Seniority","Age.of.client","Family.Situation","Profession","Home.of.employee","Size.of.savings","Active.mean","Mean.of.mouvements","Cumulative.debits","overdraft.authorized","Checkbook.not.allowed")]

# Ejecutar el an??lisis MFA
res.mfa1<-MFA (Data_mfa1, group=c(2,6,2,2), type = c(rep("n",4)), ind.sup = NULL,name.group = c("Calidad cliente","Personal/riqueza","Transacciones","Servicios adic"), num.group.sup = NULL, graph = TRUE)

# Obtener los resultados del an??lisis MFA
summary(res.mfa1)

#################################################################################


MCA(Data_mfa1, ncp = 5, ind.sup = NULL, quanti.sup = NULL,quali.sup = NULL, excl=NULL, graph = TRUE,level.ventil = 0, axes = c(1,2), row.w = NULL,method="Indicator", na.method="NA", tab.disj=NULL)
#################################################################################