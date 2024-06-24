library(readxl)
library(seasonal)
library(tseries)
library(forecast)
library(urca)
library(stargazer)
library(ggplot2)
library(TSA)
library(strucchange)


####################################################################################
#Long-term interest rate for convergence purposes - 10 years maturity, denominated in UK pound sterling - United Kingdom, United Kingdom, Monthly
swe <- read.csv("E:/ECONOMETRÍA II/Karen/ECB Data Portal_20240604030910.csv",sep = ";")
View(swe)
#Bloomberg European Dated Brent Forties Oseberg Ekofisk (BFOE) Crude Oil Spot Price - Historical close
hci <- read.csv("E:/ECONOMETRÍA II/Karen/ECB Data Portal_20240611023029.csv",sep = ";")
View(hci)



swee <- ts(swe[,3], start = c(1996), frequency = 12)
hicp <- ts(hci[,3], start = c(1996), frequency = 12)

#plot(hicp, main="Pasajeros Aerolinea", col="darkblue")
par(mfrow=c(1,2))

# Plotting the first dataset
plot(hicp, 
     main="(BFOE) Crude Oil Spot Price", 
     sub="Monthly",
     xlab="Time", 
     ylab="close",
     col="darkblue")  # Línea más gruesa
grid()

# Plotting the second dataset
plot(swee, 
     main="Long-term interest rate for convergence purposes - United Kingdom", 
     sub="Monthly",
     xlab="Time", 
     ylab="Rate",
     col="darkblue")  # Línea más gruesa
grid()
#################################################################################
summary(swee)
summary(hicp)
####################################################################################
#Pruebas de raices unitarias
# Pruebas de raíz unitaria
adf.test(swee)
pp.test(swee)
kpss.test(swee)

adf.test(hicp)
pp.test(hicp)
kpss.test(hicp)

# Transformaciones si es necesario
swee_diff <- diff(swee)
hicp_diff <- diff(hicp)

# Repruebas de raíz unitaria después de la diferenciación
adf.test(swee_diff)
pp.test(swee_diff)
kpss.test(swee_diff)

adf.test(hicp_diff)
pp.test(hicp_diff)
kpss.test(hicp_diff)

################################################################################
##Identificación
windows()
hist(swee, main="Histograma de Tasas de Interés", xlab="Tasa de Interés", col="lightblue")
hist(hicp, main="Histograma de Índice armonizado de precios al consumidor", xlab="Tasa de Interés", col="lightblue")


boxplot(swee, main="Boxplot de Tasas de Interés", ylab="Tasa de Interés")
boxplot(hicp, main="Boxplot de Índice armonizado de precios al consumidor", ylab="Índice armonizado de precios al consumidor")

windows()
par(mfrow=c(1,2))
facs <- acf(swee,main="FACS", lag.max = 15)
facs
facp <- pacf(swee,main="FACP", lag.max = 15)
facp

windows()
# ACF y PACF de la serie diferenciada
diff_swee <- diff(swee)

par(mfrow=c(1,2))
acf(diff_swee, main="ACF de la serie diferenciada")
pacf(diff_swee, main="PACF de la serie diferenciada")

################################################################################
#Modelación

library(forecast)
arima_model <- auto.arima(swee, D=1,d=1)
checkresiduals(arima_model)
fr<-forecast(arima_model, h=24)

autoplot(fr) +
  labs(title="Pronóstico de Tasa de Interés a Largo Plazo - Suecia",
       x="Tiempo",
       y="Tasa de Interés") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
        axis.title = element_text(size = 12),
        axis.text = element_text(size = 10))
################################################################################
#Estimación
# Modelo SARIMA (1,1,1)(1,1,0)[12]
sarima_model1 <- Arima(swee, order=c(1,1,1), seasonal=c(1,1,0))
summary(sarima_model1)
checkresiduals(sarima_model1)

# Modelo SARIMA (0,1,1)(0,1,1)[12]
sarima_model2 <- Arima(swee, order=c(0,1,1), seasonal=c(0,1,1))
summary(sarima_model2)
checkresiduals(sarima_model2)

# Modelo SARIMA (2,1,2)(1,1,0)[12]
sarima_model3 <- Arima(swee, order=c(2,1,2), seasonal=c(1,1,0))
summary(sarima_model3)
checkresiduals(sarima_model3)

# Modelo SARIMA (1,1,0)(0,1,1)[12]
sarima_model4 <- Arima(swee, order=c(1,1,0), seasonal=c(0,1,1))
summary(sarima_model4)
checkresiduals(sarima_model4)
stargazer("sarima_model3", type="text")
################################################################################
# Comparar AIC y BIC de los modelos
aic_values <- c(AIC(sarima_model1), AIC(sarima_model2), AIC(sarima_model3), AIC(sarima_model4))
bic_values <- c(BIC(sarima_model1), BIC(sarima_model2), BIC(sarima_model3), BIC(sarima_model4))
models <- c("SARIMA(1,1,1)(1,1,0)[12]", "SARIMA(0,1,1)(0,1,1)[12]", "SARIMA(2,1,2)(1,1,0)[12]", "SARIMA(1,1,0)(0,1,1)[12]")

comparison <- data.frame(Model=models, AIC=aic_values, BIC=bic_values)
print(comparison)

# Seleccionar el mejor modelo basado en AIC y BIC
#best_model <- sarima_model3 # Por ej

################################################################################
# Pronóstico con el mejor modelo SARIMA
sarima_forecast <- forecast(sarima_model3, h=36)

# Graficar el pronóstico
autoplot(sarima_forecast) +
  ggtitle("Pronóstico de Tasa de Interés a Largo Plazo - Suecia (SARIMA)") +
  xlab("Tiempo") +
  ylab("Tasa de Interés") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
        axis.title = element_text(size = 12),
        axis.text = element_text(size = 10))
################################################################################
# Cambios estructurales   #


# Identificación de puntos de cambio estructurales en la serie swee
bp_swee <- breakpoints(swee ~ 1)
summary(bp_swee)
plot(bp_swee)

# Graficar los puntos de cambio
plot(swee, main="Long-term interest rate for convergence purposes - Swedish krona - Sweden", 
     sub="Monthly", xlab="Time", ylab="Rate", col="darkblue")
lines(bp_swee)
grid()

################################################################################
#PRUEBAS DE COINTEGRACIÓN#
# Prueba de Johansen#

# Combinación de las series temporales
data <- cbind(swee, hicp)

# Prueba de Johansen
johansen_test <- ca.jo(data, type="trace", ecdet="const", K=2)
summary(johansen_test)
################################################################################
#Pruebas de Engle-Granger (EG)
# Regresión
reg <- lm(swee ~ hicp)
summary(reg)

# Residuales de la regresión
reg_e <- reg$residuals

# Prueba de raíz unitaria en los residuales
eg_m <- ur.df(reg_e, type="none", lags=0)
summary(eg_m)

# Cálculo directo
coint.test(swee, hicp, nlag=1)

# Otra función
e <- egcm(hicp, swee)
print(e)
summary(e)
################################################################################
#Pruebas de Phillips-Ouliaris (PO)
# Regresión
reg <- lm(swee ~ hicp)
summary(reg)

# Residuales de la regresión
reg_e <- reg$residuals

# Prueba Phillips-Ouliaris con Z-tau
po <- ur.pp(reg_e, type="Z-tau")
summary(po)

# Prueba Phillips-Ouliaris con Z-alpha
po <- ur.pp(reg_e, type="Z-alpha")
summary(po)

# Prueba Phillips-Perron con Z_tau
po <- pp.test(reg_e, type="Z_tau", lag.short=TRUE)
po

# Prueba Phillips-Perron con Z_rho
po <- pp.test(reg_e, type="Z_rho", lag.short=TRUE)
po


# Prueba con ca.po
data <- ts(cbind(swee, hicp))
po <- ca.po(data, demean="constant", type="Pz")
summary(po)

# Prueba con po.test
bfx <- as.matrix(cbind(swee, hicp))
po_ <- po.test(bfx, demean=TRUE, lshort=FALSE)
po_


################################################################################
# Prueba de cointegración de Engle-Granger
reg <- lm(swee ~ hicp)
residuals_eg <- residuals(reg)
adf.test(residuals_eg)

# Prueba de cointegración de Johansen
data <- cbind(swee, hicp)
johansen_test <- ca.jo(data, type="trace", ecdet="const", K=2)
summary(johansen_test)

# Si existe cointegración, estimar un modelo VECM
vecm <- cajorls(johansen_test)
summary(vecm)


# Pruebas de causalidad de Granger
grangertest(swee ~ hicp, order = 2)
grangertest(hicp ~ swee, order = 2)


