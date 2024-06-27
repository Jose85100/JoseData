setwd("C:/Users/Ricardo/Desktop/Econometría II")

library(stargazer)
library(nortest)
library(tseries)
library(lmtest)

library(readxl)
#DWIndicators <- read_excel("DWIndicators.xlsx")
DWIndicatorsii <- read_excel("DWIndicatorsii.xlsx")
#View(DWIndicatorsii)

DWIndicatorsiii <- ts(DWIndicatorsii, start = c(1980))

Chile <- (DWIndicatorsiii[,2])
Colombia <- (DWIndicatorsiii[,3])
Ecuador <- (DWIndicatorsiii[,4])
Mexico <- (DWIndicatorsiii[,5])
Peru <- (DWIndicatorsiii[,6])

#par(mfrow=c(2,2))
plot(Chile, main="ST Chile", col="blue")
windows()
plot(Colombia, main="ST Colombia", col="darkgreen")
windows()
plot(Ecuador, main="ST Ecuador", col="red")
windows()
plot(Mexico, main="ST Mexico",col="black")
windows()
plot(Peru, main="ST Perú",col="orange")

#mtext("Fuente:World Development Indicators", side = 1, line = -1, adj = c(0, 0.5))

summary(DWIndicatorsiii[,2])
summary(DWIndicatorsiii[,3])
summary(DWIndicatorsiii[,4])
summary(DWIndicatorsiii[,5])
summary(DWIndicatorsiii[,6])

sd(DWIndicatorsiii[,2])
sd(DWIndicatorsiii[,3])
sd(DWIndicatorsiii[,4])
sd(DWIndicatorsiii[,5])
sd(DWIndicatorsiii[,6])

summary(DWIndicatorsiii[1:10, ])
summary(DWIndicatorsiii[11:20, ])
summary(DWIndicatorsiii[21:30, ])
summary(DWIndicatorsiii[31:43, ])

for (i in seq(1, nrow(DWIndicatorsiii), 10)) {
  start_row <- i
  end_row <- min(i + 9, nrow(DWIndicatorsiii))
  # Resumen del rango de filas
  summary(DWIndicatorsiii[start_row:end_row, ])
  # Desviación estándar de cada columna
  sd(DWIndicatorsiii[start_row:end_row, ])
  # Salto de línea
  cat("\n")
}


##Data from database: World Development Indicators
##Last Updated: 02/21/2024