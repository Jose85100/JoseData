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


#install.packages(c("FactoMineR","readxl","factoextra","gridExtra","FactoClass"))
#install.packages(c("pander","ggplot2","corrplot","Rcpp","broom","dplyr"))

setwd("E:/INVESTIGACIÓN")

Empresa_cualit <- read_excel("E:/INVESTIGACIÓN/Empresa_cualit.xlsx")
Empresa <- read_excel("E:/INVESTIGACIÓN/Empresa.xlsx")


Empresa <- Empresa[Empresa$Montos_desembolsados<4.687e+09, ]
Empresa <- Empresa[Empresa$Tasa_efectiva_promedio_ponderada>2.719, ]#2.719
Empresa <- Empresa[Empresa$Número_de_créditos_desembolsados>4,]
Empresa <- Empresa[Empresa$Número_de_créditos_desembolsados<5000,]

#################################################################################################################################################
library(dplyr)

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

types <- sapply(Empresa, typeof)
print(types)
names(Empresa)

p1 <- subset(Empresa, select = c("Nombre_Entidad", "Tipo_de_persona", "Sexo", "Tamaño_de_empresa", "Tipo_de_crédito", "Tipo_de_garantía", "Producto_de_crédito", "Plazo_de_crédito", "Tasa_efectiva_promedio_ponderada", "Montos_desembolsados", "Número_de_créditos_desembolsados","Colcap","TIPM","TRM"))

p12 <- subset(Empresa, select = c("Tipo_de_persona", "Sexo", "Tamaño_de_empresa", "Tipo_de_crédito", "Tipo_de_garantía", "Plazo_de_crédito", "Tasa_efectiva_promedio_ponderada", "Montos_desembolsados", "Número_de_créditos_desembolsados","Colcap","TIPM","TRM"))


#p12 <- subset(Empresa, select = c("Nombre_Entidad", "Tipo_de_persona", "Sexo", "Tamaño_de_empresa", "Tipo_de_crédito", "Tipo_de_garantía", "Plazo_de_crédito", "Tasa_efectiva_promedio_ponderada", "Montos_desembolsados", "Número_de_créditos_desembolsados","Colcap","TIPM","TRM"))

#Características "Personales"
p13 <- subset(Empresa, select = c("Tipo_de_persona", "Sexo", "Tamaño_de_empresa","Tipo_de_garantía", "Tasa_efectiva_promedio_ponderada", "Montos_desembolsados", "Número_de_créditos_desembolsados","Colcap","TIPM","TRM"))

#Características inherentes al crédito
p14 <- subset(Empresa, select = c("Tipo_de_crédito", "Tipo_de_garantía", "Producto_de_crédito", "Plazo_de_crédito", "Tasa_efectiva_promedio_ponderada", "Montos_desembolsados", "Número_de_créditos_desembolsados","Colcap","TIPM","TRM"))

#p13+Tipo de garantía
p15 <- subset(Empresa, select = c("Tipo_de_persona", "Sexo", "Tamaño_de_empresa","Tipo_de_garantía", "Tasa_efectiva_promedio_ponderada","Plazo_de_crédito", "Montos_desembolsados", "Número_de_créditos_desembolsados","Colcap","TIPM","TRM"))




p2 <- subset(Empresa_cualit, select = c("Nombre_Entidad", "Tipo_de_persona", "Sexo", "Tamaño_de_empresa", "Tipo_de_crédito", "Tipo_de_garantía", "Producto_de_crédito", "Plazo_de_crédito"))

#Sin contemplar entidades
p21 <- subset(Empresa_cualit, select = c("Tipo_de_persona", "Sexo", "Tamaño_de_empresa", "Tipo_de_crédito", "Tipo_de_garantía", "Producto_de_crédito", "Plazo_de_crédito"))

#Información del solicitante
p22 <- subset(Empresa_cualit, select = c("Tipo_de_persona", "Sexo", "Tamaño_de_empresa", "Plazo_de_crédito"))

#Información del crédito
p23 <- subset(Empresa_cualit, select = c("Tipo_de_crédito", "Tipo_de_garantía", "Producto_de_crédito", "Plazo_de_crédito"))

#Información del crédito
p24 <- subset(Empresa_cualit, select = c("Nombre_Entidad", "Tamaño_de_empresa", "Tipo_de_garantía", "Plazo_de_crédito"))


#################################################################################################################################################
#Analisis Factorial Múltiple de las empresas
Mulfactor<-MFA (p14, group=c(4,3,3), type = c("n","s","s"), ncp = 5, name.group = NULL, graph = TRUE,row.w = NULL, axes = c(3,2), tab.comp=NULL)

eig.val <- get_eigenvalue(Mulfactor)
head(eig.val,40)
fviz_screeplot(Mulfactor)


#################################################################################################################################################
Mulcorres <- MCA(p21, ncp = 5, ind.sup = NULL, quanti.sup = NULL,
    quali.sup = NULL, excl=NULL, graph = TRUE,
    level.ventil = 0, axes = c(5,6), row.w = NULL,
    method="Indicator", na.method="NA", tab.disj=NULL)

eigenval <- get_eigenvalue(Mulcorres)

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

#################################################################################################################################################
#MODELO DE REGRESIÓN LINEAL MÚLTIPLE
#VAR DEP:Montos_desembolsados

#(exp(-0.2480394)-1)*100

Empresa1 <- subset(Empresa, select = c("Tasa_efectiva_promedio_ponderada", "Montos_desembolsados", "Número_de_créditos_desembolsados","Colcap","TIPM","TRM"))
Empresa1 <- Empresa1[Empresa1$Montos_desembolsados<4.687e+09, ]
Empresa1 <- Empresa1[Empresa1$Tasa_efectiva_promedio_ponderada>2.719, ]#2.719
Empresa1 <- Empresa1[Empresa1$Número_de_créditos_desembolsados>4,]
Empresa1 <- Empresa1[Empresa1$Número_de_créditos_desembolsados<5000,]

attach(Empresa1)
tasa_e=(Tasa_efectiva_promedio_ponderada)

MontDes=log(Montos_desembolsados)
tasae=log(tasa_e)
NumCredDes=log(Número_de_créditos_desembolsados)
TIPm=log(TIPM)
Cop=log(Colcap)

inter1=(tasa_e*Número_de_créditos_desembolsados)
inter2=(TIPM/tasa_e)

cuad1=(tasa_e*tasa_e)
cuad2=(Número_de_créditos_desembolsados*Número_de_créditos_desembolsados)
cuad3=sqrt(TIPM)

m1=lm(Montos_desembolsados~tasa_e+Número_de_créditos_desembolsados) #MCO
m2=lm(MontDes~tasa_e+Número_de_créditos_desembolsados)
m3=lm(Montos_desembolsados~tasae+NumCredDes)
m4=lm(MontDes~tasae+NumCredDes+TIPm+Cop)
m5=lm(Montos_desembolsados~tasa_e+Número_de_créditos_desembolsados+inter1+inter2)
m6=lm(Montos_desembolsados~tasa_e+Número_de_créditos_desembolsados+cuad1+cuad2)


stargazer(m1, title="Modelo1",type="latex", header=FALSE)
stargazer(m2, title="Modelo2",type="latex", header=FALSE)
stargazer(m3, title="Modelo3",type="latex", header=FALSE)
stargazer(m4, title="Modelo4",type="latex", header=FALSE)
stargazer(m5, title="Modelo5",type="latex", header=FALSE)
stargazer(m6, title="Modelo6",type="latex", header=FALSE)


stargazer(m1, title="Modelo1", type="text")
stargazer(m2, title="Modelo2", type="text")
stargazer(m3, title="Modelo3", type="text")
stargazer(m4, title="Modelo4", type="text")
stargazer(m5, title="Modelo5", type="text")
stargazer(m6, title="Modelo6", type="text")

sigma(m1)
sigma(m2)
sigma(m3)
sigma(m4)
sigma(m5)
sigma(m6)

AIC(m1)
AIC(m2)
AIC(m3)
AIC(m4)
AIC(m5)
AIC(m6)

BIC(m1)
BIC(m2)
BIC(m3)
BIC(m4)
BIC(m5)
BIC(m6)

n1 <- length(resid(m1))
n2 <- length(resid(m2)) 
n3 <- length(resid(m3)) 
n4 <- length(resid(m4)) 
n5 <- length(resid(m5)) 
n6 <- length(resid(m6)) 



hqic1 <- AIC(m1) + 2 * (n1 * log(log(n1)) / n1 - 2)
hqic1
hqic2 <- AIC(m2) + 2 * (n2 * log(log(n2)) / n2 - 2)
hqic2
hqic3 <- AIC(m3) + 2 * (n3 * log(log(n3)) / n3 - 2)
hqic3
hqic4 <- AIC(m4) + 2 * (n4 * log(log(n4)) / n4 - 2)
hqic4
hqic5 <- AIC(m5) + 2 * (n5 * log(log(n5)) / n5 - 2)
hqic5
hqic6 <- AIC(m6) + 2 * (n6 * log(log(n6)) / n6 - 2)
hqic6

#MODELO ELEGIDO: 4
#Validación de supuestos
#NORMALIDAD
library(bbmle)
# Definir la función de log-verosimilitud
ll <- function(beta0, beta1, beta2, mu, sigma) {
  R <- MontDes - tasae * beta1 - NumCredDes * beta2 - beta0
  -sum(dnorm(R, mean = mu, sd = sigma, log = TRUE))
}
# Inicializar valores
start_vals <- list(beta0 = 1, beta1 = 0, beta2 = 0, mu = 10, sigma = 1000)
# Ajustar el modelo de máxima verosimilitud
m4 <- mle2(ll, start = start_vals)
# Mostrar resultados
summary(m4)

m4_as_lm <- update(m4, method = "BFGS")
# Presentar los resultados con stargazer
stargazer(m4_as_lm, title="Modelo4", type="text")


#HOMOCEDASTICIDAD
error=residuals(m4)
error2=error^2
plot(tasae,error2)
cov(tasae,error2)
windows()
plot(NumCredDes,error2)
cov(NumCredDes,error2)
library(lmtest)
bptest(m4)
library(car)
ncvTest(m4)

#Error estandar robusto
library(sandwich)
coeftest(m4, vcov = vcovHC)

m4.robusto = rlm(MontDes ~tasae+NumCredDes+TIPm+Cop+inter2+cuad3, data = Empresa1)
ncvTest(m4.robusto)

#Mínimos cuadrados generalizado
library(stats)
m4.glm <- glm(MontDes ~tasae+NumCredDes+TIPm+Cop+inter2+cuad3, family = "gaussian")
bptest(m4.glm)

#Mínimoos cuadrados ponderados
m4.wls = lm(MontDes~tasae+NumCredDes+TIPm+Cop+inter2+cuad3, weights = 1/(resid(m4)^2))
ncvTest(m4.wls)
bptest(m4.wls)

#EER
library(lmtest)
library(tseries)
library(sandwich)
coeftest(m4.wls,vcoc=vcovHC)

#NO MULTICOLINEALIDAD
vif(m4)

#ESPECIFICACIÓN CORRECTA
#Estadístico ML=n*R^2
#Estadístico ML=38285*0.08836>Chi cuadrado (7.81)==> mal especificado
qchisq(0.95,3) #==>7.81
resettest(m4.wls) #pvalue=0.4199>0.05 ==> modelo correcto

#NORMALIDAD

error <- residuals(m4)
library(kdensity)
library(tseries)
windows()
plot(density(error), col = "red", ylim = c(0, 0.5))
curve(dnorm(x, mean(error), sd(error)), col = "blue", lwd = 3, add = TRUE)
curve(dnorm(x, mean=0, sd=1), from=-4, to=4, col="blue", lty=1,
      xlab="Valores", ylab="Densidad de Probabilidad",
      main="Distribución Normal estándar",add = TRUE)
jarque.bera.test(error)
ks.test(error, "pnorm", exact = FALSE)


jarque.bera.test(error)
ks.test(error, "pnorm", exact = FALSE)

resultado_jb <- jarque.bera.test(error)
print(resultado_jb)


# Estimamos el modelo
m4 <- lm(MontDes ~ tasae + NumCredDes + TIPm + Cop + inter2 + cuad3)
# Encontramos el valor óptimo para lambda
boxcox_result <- boxcox(m4)
# Valor óptimo de lambda
lambda <- boxcox_result$x[which.max(boxcox_result$y)]
# Transformamos la variable de respuesta con Box-Cox
MontDes_transformed <- (MontDes^lambda - 1) / lambda
# Estimamos el modelo nuevamente con la variable transformada
m4_transformed <- lm(MontDes_transformed ~ tasae + NumCredDes + TIPm + Cop + inter2 + cuad3)
ncvTest(m4_transformed)
#Corrección minimos cuadrados ponderados
m4.wls = lm(MontDes_transformed~tasae+NumCredDes+TIPm+Cop+inter2+cuad3, weights = 1/(resid(m4)^2))
ncvTest(m4.wls)
bptest(m4.wls)


errores <- residuals(m4.wls)
jarque.bera.test(errores)
ks.test(errores, "pnorm", exact = FALSE)


plot(density(errores), col = "red", ylim = c(0, 0.8))
curve(dnorm(x, mean(errores), sd(errores)), col = "blue", lwd = 3, add = TRUE)
curve(dnorm(x, mean=0, sd=1), from=-4, to=4, col="blue", lty=1,
      xlab="Valores", ylab="Densidad de Probabilidad",
      main="Distribución Normal estándar",add = TRUE)


##VALIDACIONES ADD
fitmod<- fitted(m4.wls)
resimod<- residuals(m4.wls)
restud<- rstudent(m4.wls)

### Normalidad
ks.test(restud, "pnorm")
hist(restud, xlab = "residuos", main = "histograma residuos")

### Homogeneidad de varianzas
library(lmtest)
bptest(m4.wls, studentize = FALSE, data = Empresa1)

modelo <- lm(y ~ x1 + x2, data = tu_data)
corregido <- coeftest(modelo, vcov = vcovHC(modelo, type = "HC1"))

### Autocorrelación
dwtest(m4.wls, alternative = "two.sided", data = Empresa1)

# Ajustar el modelo ponderado
m4.wls <- lm(MontDes ~ tasae + NumCredDes, weights = 1/(resid(m4)^2), data = Empresa1)
residuos_ponderados <- resid(m4.wls) * sqrt(1/(resid(m4.wls)^2))
dw_est <- sum(diff(residuos_ponderados)^2) / sum(residuos_ponderados^2)
p_valor_dw <- 2 * (1 - pnorm(abs(dw_est)))
cat("Estadística de Durbin-Watson:", dw_est, "\n")
cat("Valor p de la prueba de Durbin-Watson:", p_valor_dw, "\n")

#Valores Atípicos
outlierTest(m4.wls)
influence_measures <- influence.measures(m4.wls)
summary(influence_measures)
influencePlot(m4.wls, id.n = 2)

Empresa1[28317,]
Empresa1[33502,]

# Multicolinealidad
library(car)
vif(m4.wls)
sqrt(vif(m4.wls)) > 2


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

Empresa2 <- subset(Empresa, select = c("Tasa_efectiva_promedio_ponderada", "Montos_desembolsados", "Número_de_créditos_desembolsados","Tipo_de_persona","Sexo","Tipo_de_garantía","Plazo_de_crédito","Colcap","TIPM","TRM"))
Empresa2 <- Empresa2[Empresa2$Montos_desembolsados < 4.687e+09, ]
Empresa2 <- Empresa2[Empresa2$Tasa_efectiva_promedio_ponderada > 2.719, ]
Empresa2 <- Empresa2[Empresa2$Número_de_créditos_desembolsados > 4,]
Empresa2 <- Empresa2[Empresa2$Número_de_créditos_desembolsados < 5000,]

attach(Empresa2)

tasa_e <- Empresa2$Tasa_efectiva_promedio_ponderada
MontDes <- log(Empresa2$Montos_desembolsados)

TipPer <- ifelse(Empresa2$Tipo_de_persona == "Natural", 1, 0)
Sexgen <- ifelse(Empresa2$Sexo == "Femenino", 1, 0)
Tipga <- ifelse(Empresa2$Tipo_de_garantía == "Sin Garantía", 1, 0)
PlazG <- ifelse(Empresa2$Plazo_de_crédito == "Plazos Medios", 1, 0)


mc1=lm(Montos_desembolsados~tasa_e+Número_de_créditos_desembolsados+TipPer+Sexgen+Tipga+PlazG+TIPM+Colcap+TRM) #MCO
mc2=lm(MontDes~tasa_e+Número_de_créditos_desembolsados+TipPer+Sexgen+Tipga+PlazG+TIPM+Colcap+TRM)


stargazer(mc1, title="Modelo de Regresión Lineal1", type="text")
stargazer(mc2, title="Modelo de Regresión Lineal", type="text")

stargazer(mc1, title="Modelo6",type="latex", header=FALSE)
stargazer(mc2, title="Modelo6",type="latex", header=FALSE)

stargazer(modelo_mle, title="Modelo6",type="latex", header=FALSE)

sigma(mc1)
sigma(mc2)
AIC(mc1)
AIC(mc2)
BIC(mc1)
BIC(mc2)

ll <- function(beta0, beta1, beta2, beta3, beta4, beta5, beta6, beta7, beta8, mu, sigma) {
  R <- MontDes - beta1 * tasa_e - beta2 * Número_de_créditos_desembolsados -
    beta3 * TipPer - beta4 * Sexgen - beta5 * Tipga - beta6 * PlazG -
    beta7 * TIPm - beta8 * Cop - beta0
  -sum(dnorm(R, mean = mu, sd = sigma, log = TRUE))
}
# Inicializar valores
start_vals <- list(
  beta0 = 1, beta1 = 0, beta2 = 0, beta3 = 0, beta4 = 0, beta5 = 0, beta6 = 0, beta7 = 0, beta8 = 0,
  mu = 0, sigma = 1
)
# Ajustar el modelo de máxima verosimilitud
modelo_mle <- mle2(ll, start = start_vals)
# Mostrar resultados
summary(modelo_mle)

modelo_broom <- tidy(modelo_mle)
latex_model <- screenreg(modelo_broom)
cat(latex_model)

#NORMALIDAD
errores <- residuals(mc2)
jarque.bera.test(errores)
ks.test(errores, "pnorm",mean=mean(errores),sd=sd(errores))
plot(density(errores), col = "red", ylim = c(0, 0.8))
curve(dnorm(x, mean(errores), sd(errores)), col = "blue", lwd = 3, add = TRUE)
curve(dnorm(x, mean=0, sd=1), from=-4, to=4, col="blue", lty=1,
      xlab="Valores", ylab="Densidad de Probabilidad",
      main="Distribución Normal estándar",add = TRUE)

error <- residuals(mc2)
jarque.bera.test(error)
ks.test(error, "pnorm", exact = FALSE)

#HOMOCEDASTICIDAD
ncvTest(mc2)
bptest(mc2)

# Correccion HT
# Errores estandar robustos
library(sandwich)
mc22<-coeftest(mc2, vcov = vcovHC)

#MULTICOLINEALIDAD
vif(mc2)

#ESPECIFICACIÓN CORRECTA
resettest(mc2)

#Autocorrelación
dwtest(mc2, alternative = "two.sided", data = Empresa1)

#################################################################################################################################################
#MODELO LINEAL DE PROBABILIDAD
#Var Dep: Tipo de persona
TipPer=ifelse(Tipo_de_persona=="Natural",1,0)
table(TipPer)
prop.table(table(TipPer))

mlp=lm(TipPer~Montos_desembolsados+tasa_e+Número_de_créditos_desembolsados)
#beta1: Si la tasa de interés aumentan en 1 ==> la probabilidad de ser
#persona natural disminuye en 0.28%

#si la tasa de interés aumenta de 5% a 6%, la probabilidad de que una 
#observación sea clasificada como persona natural disminuirá 
#de 50% a 49,72%.

modlogit=glm(informal~esc+exper,family = binomial(link="logit"))

modprobit=glm(informal~esc+exper,family=binomial(link="probit"))


#################################################################################################################################################

#################################################################################################################################################
