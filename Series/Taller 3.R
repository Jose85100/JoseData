######################################################
######### Econometría II - Series de Tiempo ##########
########### Simulación de un Proceo AR(2) ############
######################################################
n<-1000000
e <- rnorm(n,0,sqrt(1))
y<-e
for(t in 3:n) y[t]<-1+0.6*y[t-1]+0.2*y[t-2]+e[t]
AR21<-ts(y)
par(mfrow=c(1,1))
#ts.plot(AR21, main="Proceso AR(2)")
summary(AR21)
var(AR21)
sd(AR21)

par(mfrow=c(1,2))
facs1 <- acf(AR21, main="FACS", lag.max = 10, ylim=c(-1,1))
facs1
facp1 <- pacf(AR21, main="FACP", lag.max = 10, ylim=c(-1,1))
facp1
######################################################
n<-1000000
e <- rnorm(n,0,sqrt(1))
y<-e
for(t in 3:n) y[t]<-1+0.2*y[t-1]+0.6*y[t-2]+e[t]
AR22<-ts(y)
par(mfrow=c(1,1))
#ts.plot(AR22, main="Proceso AR(2)")
summary(AR22)
var(AR22)
sd(AR22)

par(mfrow=c(1,2))
facs2 <- acf(AR22, main="FACS", lag.max = 10, ylim=c(-1,1))
facs2
facp2 <- pacf(AR22, main="FACP", lag.max = 10, ylim=c(-1,1))
facp2
######################################################

######################################################
######### Econometría II - Series de Tiempo ##########
########### Simulación de un Proceo MA(2) ############
######################################################

n<-1000000
e <- rnorm(n,0,sqrt(1))
y<-e
for(t in 3:n) y[t]<-1+0.6*e[t-1]+0.2*e[t-2]+e[t]
MA21<-ts(y)
ts.plot(MA21, main="Proceso MA(2)")
summary(MA21)
var(MA21)
sd(MA21)

par(mfrow=c(1,2))
facs3 <- acf(MA21, main="FACS", lag.max = 10, ylim=c(-1,1))
facs3
facp3 <- pacf(MA21, main="FACP", lag.max = 10, ylim=c(-1,1))
facp3

######################################################
n<-1000000
e <- rnorm(n,0,sqrt(1))
y<-e
for(t in 3:n) y[t]<-1+0.2*e[t-1]+0.6*e[t-2]+e[t]
MA22<-ts(y)
ts.plot(MA22, main="Proceso MA(2)")
summary(MA22)
var(MA22)
sd(MA22)

par(mfrow=c(1,2))
facs4 <- acf(MA22, main="FACS", lag.max = 10, ylim=c(-1,1))
facs4
facp4 <- pacf(MA22, main="FACP", lag.max = 10, ylim=c(-1,1))
facp4

######################################################
Fama <- read_excel("C:/Users/Ricardo/Desktop/Econometría II/2 .Fama.xls")


######################################################