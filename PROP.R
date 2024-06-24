library(ade4)
library(FactoMineR)
library(factoextra)
library(readr)
library(readxl)

df_1 <- read_excel("E:/IDE/BI/df_1.xlsx")
View(df_1)

names(df_1)

p1 <- subset(df_1, select = c("Nombre_Entidad", "Tipo_de_persona", "Sexo","Tamaño_de_empresa", "Tipo_de_crédito", "Tipo_de_garantía", "Plazo de crédito","Antiguedad_de_la_empresa", "Tipo_de_Tasa","Rango_monto_desembolsado", "Clase_deudor","Tasa_efectiva_promedio_ponderada", "margen_adicional","Montos_desembolsados", "Numero_de_creditos_desembolsados"))

p2 <- subset(df_1, select = c("Nombre_Entidad", "Tipo_de_persona", "Sexo","Tamaño_de_empresa", "Tipo_de_crédito", "Tipo_de_garantía", "Plazo de crédito","Antiguedad_de_la_empresa", "Tipo_de_Tasa","Rango_monto_desembolsado", "Clase_deudor"))

#################################################################################################################################################
#Analisis Factorial Múltiple de las empresas

Mulfactor<-MFA (p1, group=c(1,3,7,4), type = c("n","n","n","s"), ncp = 5, name.group = NULL, graph = TRUE,row.w = NULL, axes = c(1,2), tab.comp=NULL)

eig.val <- get_eigenvalue(Mulfactor)
head(eig.val,40)
fviz_screeplot(Mulfactor)

#################################################################################################################################################
Mulcorres <- MCA(p2, ncp = 5, ind.sup = NULL, quanti.sup = NULL,
    quali.sup = NULL, excl=NULL, graph = TRUE,
    level.ventil = 0, axes = c(1,2), row.w = NULL,
    method="Indicator", na.method="NA", tab.disj=NULL)

eigenval <- get_eigenvalue(Mulcorres)
#################################################################################################################################################
# Convertir a factores
datos$sexo <- as.factor(datos$sexo)
datos$tamaño_empresa <- as.factor(datos$tamaño_empresa)

# Ajustar el modelo de regresión logística
modelo_logit <- glm(y ~ x1 + sexo + tamaño_empresa, data = datos, family = binomial(link = "logit"))

# Resumen del modelo logit
summary(modelo_logit)

# Ajustar el modelo de regresión probit
modelo_probit <- glm(y ~ x1 + sexo + tamaño_empresa, data = datos, family = binomial(link = "probit"))

# Resumen del modelo probit
summary(modelo_probit)

# Hacer predicciones con el modelo logit
predicciones_logit <- predict(modelo_logit, type = "response")

# Hacer predicciones con el modelo probit
predicciones_probit <- predict(modelo_probit, type = "response")

# Mostrar las primeras predicciones
head(predicciones_logit)
head(predicciones_probit)