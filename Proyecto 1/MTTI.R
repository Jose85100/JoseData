#################################################################################################################################################
library(FactoMineR)
library(readxl)
library("factoextra")
library(lmtest)
library(robustbase)

library(dplyr)
library(MASS)
library(stargazer)

library(bbmle)

library(dplyr)
library(car)
library(MASS)
library(stargazer)
library(lmtest)
library(tseries)
library(sandwich)
library(car)
library(kdensity)
library(bbmle)


#install.packages(c("FactoMineR","readxl","factoextra","gridExtra","FactoClass"))
#install.packages(c("pander","ggplot2","corrplot","Rcpp","broom","dplyr"))

setwd("E:/INVESTIGACIÓN")

Empresa_cualit <- read_excel("E:/INVESTIGACIÓN/Empresa_cualit.xlsx")
Empresa <- read_excel("E:/INVESTIGACIÓN/Empresa.xlsx")

#################################################################################################################################################

Empresa <- Empresa %>%
  rename(
    'Tipo_de_persona' = '(1)Tipo_de_persona',
    'Sexo' = '(2)Sexo',
    'Tamaño_de_empresa' = '(3)Tamaño_de_empresa',
    'Tipo_de_crédito' = '(4)Tipo_de_crédito',
    'Tipo_de_garantía' = '(5)Tipo_de_garantía',
    'Producto_de_crédito' = '(6) Producto de crédito',
    'Plazo_de_crédito' = '(7) Plazo de crédito',
    'Tasa_efectiva_promedio_ponderada' = '(8)Tasa_efectiva_promedio_ponderada',
    'Montos_desembolsados' = '(10)Montos_desembolsados',
    'Número_de_créditos_desembolsados' = '(11)Número_de_créditos_desembolsados'
  )

Empresa_cualit<- Empresa_cualit %>%
  rename(
    'Tipo_de_persona' = '(1)Tipo_de_persona',
    'Sexo' = '(2)Sexo',
    'Tamaño_de_empresa' = '(3)Tamaño_de_empresa',
    'Tipo_de_crédito' = '(4)Tipo_de_crédito',
    'Tipo_de_garantía' = '(5)Tipo_de_garantía',
    'Producto_de_crédito' = '(6) Producto de crédito',
    'Plazo_de_crédito' = '(7) Plazo de crédito'
)



#################################################################################################################################################

Empresa2 <- subset(Empresa, select = c("Tasa_efectiva_promedio_ponderada", "Montos_desembolsados", "Número_de_créditos_desembolsados","Tipo_de_persona","Sexo","Tamaño_de_empresa","Tipo_de_garantía","Plazo_de_crédito","Colcap","TIPM","TRM"))

Empresa2 <- Empresa2[Empresa2$Montos_desembolsados < 1e+11, ]
Empresa2 <- Empresa2[Empresa2$Tasa_efectiva_promedio_ponderada > 6, ]
Empresa2 <- Empresa2[Empresa2$Tasa_efectiva_promedio_ponderada < 42, ]
Empresa2 <- Empresa2[Empresa2$Número_de_créditos_desembolsados >5,]
Empresa2 <- Empresa2[Empresa2$Número_de_créditos_desembolsados < 1600,]

#################################################################################################################################################
#MODELO DE REGRESIÓN LINEAL MÚLTIPLE CON VAR DIC
#VAR DEP:Montos_desembolsados
library(dplyr)
library(car)
library(MASS)
library(stargazer)
library(lmtest)
library(tseries)
library(sandwich)
library(car)
library(kdensity)
library(bbmle)


attach(Empresa2)

tasa_e <- Empresa2$Tasa_efectiva_promedio_ponderada
MontDes <- log(Empresa2$Montos_desembolsados)

TipPer <- ifelse(Empresa2$Tipo_de_persona == "Juridica", 1, 0)
Sexgen <- ifelse(Empresa2$Sexo == "Femenino", 1, 0)
Tipga <- ifelse(Empresa2$Tipo_de_garantía == "Sin Garantía", 1, 0)
PlazG <- ifelse(Empresa2$Plazo_de_crédito == "Plazos Medios", 1, 0)
TamE<-ifelse(Empresa2$Tamaño_de_empresa == "Gran empresa", 1, 0)
tase<-log(tasa_e)

mc1=lm(Montos_desembolsados~tase+Número_de_créditos_desembolsados+TipPer+Sexgen+Tipga+TamE+PlazG+TIPM+Colcap)
mc2=lm(MontDes~tase+Número_de_créditos_desembolsados+TipPer+Sexgen+Tipga+TamE+PlazG+TIPM+Colcap)

mean(tase)
mean(Número_de_créditos_desembolsados)
mean(TIPM)
mean(Colcap)

#################################################################################################################################################

#################################################################################################################################################

#LMD1=tase+Número_de_créditos_desembolsados+TipPer+Sexgen+Tipga+TamE+PlazG+TIPM+Colcap
#################################################################################################################################################
#PERSONA JURÍDICA, (FEMENINO), SIN GARANTÍA, PLAZO MEDIO, GRAN EMPRESA#estado inicial#
LMD=27.359-(2.541*3.126558)+(0.002*136.1147)+(0.189)-(0.064)-(0.154)+(0.834)+(0.631)+(0.158*9.665938)-(0.001*1251.611)

#j#PERSONA JURÍDICA, (NO FEMENINO), SIN GARANTÍA, PLAZO MEDIO, GRAN EMPRESA
LMDj=27.359-(2.541*3.126558)+(0.002*136.1147)+(0.189)-(0.154)+(0.834)+(0.631)+(0.158*9.665938)-(0.001*1251.611)

Ob1=LMD-LMD1
Ob1
(exp(Ob1)-1)*100

#################################################################################################################################################

LMD1=27.359-(2.541*3.126558)+(0.002*136.1147)-(0.064)+(0.631)+(0.158*9.665938)-(0.001*1251.611)

LMD2=27.359-(2.541*3.126558)+(0.002*136.1147)+(0.631)+(0.834)+(0.158*9.665938)-(0.001*1251.611)


Ob1=LMD1-LMD2
Ob1
(exp(Ob1)-1)*100
#################################################################################################################################################

#################################################################################################################################################

stargazer(mc1, title="Modelo de Regresión Lineal1", type="text")
stargazer(mc2, title="Modelo de Regresión Lineal", type="text")

stargazer(mc1, title="Modelo6",type="latex", header=FALSE)
stargazer(mc2, title="Modelo6",type="latex", header=FALSE)


sigma(mc1)
sigma(mc2)
AIC(mc1)
AIC(mc2)
BIC(mc1)
BIC(mc2)


#NORMALIDAD
errores <- residuals(mc2)
#jarque.bera.test(errores)
#ks.test(errores, "pnorm",mean(errores),sd(errores))
plot(density(errores), col = "red", ylim = c(0, 0.5))
curve(dnorm(x, mean(errores), sd(errores)), col = "green", lwd = 2, add = TRUE)
curve(dnorm(x, mean=0, sd=1), from=-4, to=4, col="blue", lty=1,
      xlab="Valores", ylab="Densidad de Probabilidad",
      main="Distribución Normal estándar",add = TRUE)

shapiro.test(errores)
# Gráfico Q-Q
qqnorm(errores)
qqline(errores)


#NORMALIDAD
errores1 <- residuals(m4.robusto)
#jarque.bera.test(errores1)
#ks.test(errores1, "pnorm",mean(errores1),sd(errores1))
plot(density(errores1), col = "red", ylim = c(0, 0.8))
curve(dnorm(x, mean(errores1), sd(errores1)), col = "green", lwd = 2, add = TRUE)
curve(dnorm(x, mean=0, sd=1), from=-4, to=4, col="blue", lty=1,
      xlab="Valores", ylab="Densidad de Probabilidad",
      main="Distribución Normal estándar",add = TRUE)

m4.robusto = rlm(MontDes~tase+Número_de_créditos_desembolsados+TipPer+Sexgen+Tipga+TamE+PlazG+TIPM+Colcap, data = Empresa2)
ncvTest(m4.robusto)


errores3 <- residuals(m4.wls)
jarque.bera.test(error)
ks.test(errores3, "pnorm",mean(errores3),sd(errores3))



#HOMOCEDASTICIDAD
ncvTest(mc2)
bptest(mc2)



#Mínimoos cuadrados ponderados
m4.wls = lm(MontDes~tase+Número_de_créditos_desembolsados+Sexgen+TipPer+Tipga+TamE+PlazG+TIPM+Colcap, weights = 1/(resid(mc2)^2))
ncvTest(m4.wls)
bptest(m4.wls)
errore <- residuals(m4.wls)
ks.test(errore, "pnorm",mean(errore),sd(errore))

stargazer(m4.wls, title="Modelo de Regresión", type="text")

stargazer(m4.wls, title="Modelo",type="latex", header=FALSE)


# Correccion HT
# Errores estandar robustos
library(sandwich)
mc22<-coeftest(m4.wls, vcov = vcovHC)

#MULTICOLINEALIDAD
vif(mc2)
vif(mc22)
vif(m4.wls)

#ESPECIFICACIÓN CORRECTA
resettest(mc2)
resettest(m4.wls)

#Autocorrelación
dwtest(mc2, alternative = "two.sided", data = Empresa2)
dwtest(m4.wls, alternative = "two.sided", data = Empresa2)


#################################################################################################################################################


Empresa <- Empresa %>%
  mutate(
    Nombre_Entidad = as.factor(Nombre_Entidad),
    Tipo_de_persona = as.factor(Tipo_de_persona),
    Sexo = as.factor(Sexo),
    Tamaño_de_empresa = as.factor(Tamaño_de_empresa),
    Tipo_de_crédito = as.factor(Tipo_de_crédito),
    Tipo_de_garantía = as.factor(Tipo_de_garantía),
    Producto_de_crédito = as.factor(Producto_de_crédito),
	Plazo_de_crédito = as.factor(Plazo_de_crédito)
  )

lista_de_variables <- list(
  Nombre_Entidad = levels(Empresa$Nombre_Entidad),
  Tipo_de_persona = levels(Empresa$Tipo_de_persona),
  Sexo = levels(Empresa$Sexo),
  Tamaño_de_empresa = levels(Empresa$Tamaño_de_empresa),
  Tipo_de_crédito = levels(Empresa$Tipo_de_crédito),
  Tipo_de_garantía = levels(Empresa$Tipo_de_garantía),
  Producto_de_crédito = levels(Empresa$Producto_de_crédito),Plazo_de_crédito = levels(Empresa$Plazo_de_crédito)
)

print(lista_de_variables)





