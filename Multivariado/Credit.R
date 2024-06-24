#################################################################################
# Cargar bibliotecas necesarias
library(FactoMineR)
library(cluster)
library(readxl)

#################################################################################
setwd("F:/MATEMÁTICA/Métodos estadísticos multivariados")

Credit <- read.csv("Credit.csv", header = TRUE)

Credit_1 <- Credit[, !(names(Credit) %in% c("Variable.continuous.1", "Variable.continuous.2"))]
#################################################################################

# Crear un dataframe con las variables categ??ricas
data_mca <- Credit_1[, c("Type.of.client", "Age.of.client", "Family.Situation","Seniority", "Home.of.employee", "Size.of.savings", "Profession", "Active.mean", "Mean.of.mouvements", "Cumulative.debits", "overdraft.authorized", "Checkbook.not.allowed")]
# Realizar el MCA
result_mca <- MCA(data_mca, graph = TRUE)
#################################################################################

# Realizar K-Means (ejemplo con 3 cl??steres)
kmeans_clusters <- kmeans(result_mca$ind$coord, centers = 3)

# Mostrar los resultados de K-Means
print(kmeans_clusters)

#################################################################################
# Crear la variable "group" como un factor a partir de la variable "Type.of.client"
Data_mfa <- Credit_1
Data_mfa <- Data_mfa[, c("Seniority","Mean.of.mouvements","Cumulative.debits","Age.of.client", "Family.Situation","Profession","Home.of.employee","Size.of.savings","Active.mean","Type.of.client","Checkbook.not.allowed","overdraft.authorized")]

# Ejecutar el an??lisis MFA
MFA (Data_mfa, group=c(3,3,3,3), type = c(rep("n",4)), ind.sup = NULL,name.group = c("Transaccional","Personal","Ingresos/Riqueza","Relación banco"), num.group.sup = NULL, graph = TRUE)

# Obtener los resultados del an??lisis MFA
summary(res.mfa)

#################################################################################

#table(Credit_1$Iden)
table(Credit_1$Type.of.client)
table(Credit_1$Age.of.client)
table(Credit_1$Family.Situation)
table(Credit_1$Seniority)
table(Credit_1$Home.of.employee)
table(Credit_1$Size.of.savings)
table(Credit_1$Profession)
table(Credit_1$Active.mean)
table(Credit_1$Mean.of.mouvements)
table(Credit_1$Cumulative.debits)
table(Credit_1$overdraft.authorized)
table(Credit_1$Checkbook.not.allowed)
