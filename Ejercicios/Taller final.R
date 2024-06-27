#Trabajo final Introducción a la econometría
#Jose Gabriel Orosco
#Karen Magnolia Parra
setwd("C:/Users/Ricardo/Desktop/Taller final/2020")
library(readr)
library(haven)
library(readxl)
library(stargazer)

#Llamar la base de datos
data <- read.csv("C:/Users/Ricardo/Desktop/Taller final/2020/EAM_2020.CSV", sep = ";")
data
attach(data)

#Regresión normal
a1=data$POHM
a2=data$TSSPP
a3=data$CONSMATE
a4=data$EELEC
a5=data$INVEBRTA
a6=data$TCGTMP
b0=data$VALAGRI
it1=data$POHM*data$EELEC
it2=data$INVEBRTA*data$POHM

#it1=a1*a4
#it2=a5*a1


#Dicotomas
table(dum1)
prop.table(table(dum1))*100
###############################################################################

#Modelo lineal con interacción y dummys
m1=lm(b0~a1+a2+a3+a4+a5+a6+it1+it2+dum1+dum2)
#summary(m1)
stargazer(m1, type="text",out="modelo lineal")
#resultado_anova <- anova(m2)
#tabla_anova <- stargazer(resultado_anova, type = "text")
anova(m1)

###############################################################################

#Modelo log lin con interacción y dummys
lb0=log((data$VALAGRI))
m2=lm(lb0~a1+a2+a3+a4+a5+a6+it1+it2+dum1+dum2)
#summary(m1)
stargazer(m2, type="text",out="modelo lineal")
#resultado_anova <- anova(m2)
#tabla_anova <- stargazer(resultado_anova, type = "text")
anova(m2)

###############################################################################

#Modelo lin-log con interacción y dummys
ita=log(data$POHM)*log(data$EELEC)
itb=log(data$INVEBRTA)*log(data$POHM)
m3=lm(b0~log(a1)+log(a2)+log(a3)+log(a4)+log(a5)+log(a6)+ita+itb+dum1+dum2)
summary(m3)
stargazer(m3, type="text",out="modelo lineal")
#resultado_anova <- anova(m3)
#tabla_anova <- stargazer(resultado_anova, type = "text")
###############################################################################

#Modelo log-log con interacción y dummys
lb0=log((data$VALAGRI))
ita=(data$POHM)*(data$EELEC)#log(data$POHM)*log(data$EELEC)
itb=(data$INVEBRTA)*(data$POHM)#log(data$INVEBRTA)*log(data$POHM)
m4=lm(lb0~log(a1)+log(a2)+log(a3)+log(a4)+log(a5)+log(a6)+ita+itb+dum1+dum2)
summary(m4)
stargazer(m4, type="text",out="modelo lineal")
#resultado_anova <- anova(m3)
#tabla_anova <- stargazer(resultado_anova, type = "text")

vm1 <- sigma(m1)^2
print(vm1)
vm2 <- sigma(m2)^2
print(vm2)
vm3 <- sigma(m3)^2
print(vm3)
vm4 <- sigma(m4)^2
print(vm4)

AIC(m1);BIC(m1);AIC(m2);BIC(m2)
AIC(m3);BIC(m3);AIC(m4);BIC(m4)

# Deteccion con coeficiente de correlacion a1
cor1 <- cor(a1,a1,use = "complete.obs");print(cor);cor2 <- cor(a1,a2,use = "complete.obs");print(cor);
cor3 <- cor(a1,a3,use = "complete.obs");print(cor);cor4 <- cor(a1,a4,use = "complete.obs");print(cor);
cor5 <- cor(a1,a5,use = "complete.obs");print(cor);cor6 <- cor(a1,a6,use = "complete.obs");print(cor);
cor7 <- cor(a1,dum1,use = "complete.obs");print(cor);cor8 <- cor(a1,dum2,use = "complete.obs");print(cor)

# Deteccion con coeficiente de correlacion a2
cor1 <- cor(a2,a1,use = "complete.obs");print(cor1);cor2 <- cor(a2,a2,use = "complete.obs");print(cor2);
cor3 <- cor(a2,a3,use = "complete.obs");print(cor3);cor4 <- cor(a2,a4,use = "complete.obs");print(cor4);
cor5 <- cor(a2,a5,use = "complete.obs");print(cor5);cor6 <- cor(a2,a6,use = "complete.obs");print(cor6);
cor7 <- cor(a2,dum1,use = "complete.obs");print(cor7);cor8 <- cor(a2,dum2,use = "complete.obs");print(cor8)

# Deteccion con coeficiente de correlacion a3
cor1 <- cor(a3,a1,use = "complete.obs");print(cor1);cor2 <- cor(a3,a2,use = "complete.obs");print(cor2);
cor3 <- cor(a3,a3,use = "complete.obs");print(cor3);cor4 <- cor(a3,a4,use = "complete.obs");print(cor4);
cor5 <- cor(a3,a5,use = "complete.obs");print(cor5);cor6 <- cor(a3,a6,use = "complete.obs");print(cor6);
cor7 <- cor(a3,dum1,use = "complete.obs");print(cor7);cor8 <- cor(a3,dum2,use = "complete.obs");print(cor8)

# Deteccion con coeficiente de correlacion a4
cor1 <- cor(a4,a1,use = "complete.obs");print(cor1);cor2 <- cor(a4,a2,use = "complete.obs");print(cor2);
cor3 <- cor(a4,a3,use = "complete.obs");print(cor3);cor4 <- cor(a4,a4,use = "complete.obs");print(cor4);
cor5 <- cor(a4,a5,use = "complete.obs");print(cor5);cor6 <- cor(a4,a6,use = "complete.obs");print(cor6);
cor7 <- cor(a4,dum1,use = "complete.obs");print(cor7);cor8 <- cor(a4,dum2,use = "complete.obs");print(cor8)

# Deteccion con coeficiente de correlacion a5
cor1 <- cor(a5,a1,use = "complete.obs");print(cor1);cor2 <- cor(a5,a2,use = "complete.obs");print(cor2);
cor3 <- cor(a5,a3,use = "complete.obs");print(cor3);cor4 <- cor(a5,a4,use = "complete.obs");print(cor4);
cor5 <- cor(a5,a5,use = "complete.obs");print(cor5);cor6 <- cor(a5,a6,use = "complete.obs");print(cor6);
cor7 <- cor(a5,dum1,use = "complete.obs");print(cor7);cor8 <- cor(a5,dum2,use = "complete.obs");print(cor8)

# Deteccion con coeficiente de correlacion a6
cor1 <- cor(a6,a1,use = "complete.obs");print(cor1);cor2 <- cor(a6,a2,use = "complete.obs");print(cor2);
cor3 <- cor(a6,a3,use = "complete.obs");print(cor3);cor4 <- cor(a6,a4,use = "complete.obs");print(cor4);
cor5 <- cor(a6,a5,use = "complete.obs");print(cor5);cor6 <- cor(a6,a6,use = "complete.obs");print(cor6);
cor7 <- cor(a6,dum1,use = "complete.obs");print(cor7);cor8 <- cor(a6,dum2,use = "complete.obs");print(cor8)

# Deteccion con coeficiente de correlacion dum1
cor1 <- cor(dum1,a1,use = "complete.obs");print(cor1);cor2 <- cor(dum1,a2,use = "complete.obs");print(cor2);
cor3 <- cor(dum1,a3,use = "complete.obs");print(cor3);cor4 <- cor(dum1,a4,use = "complete.obs");print(cor4);
cor5 <- cor(dum1,a5,use = "complete.obs");print(cor5);cor6 <- cor(dum1,a6,use = "complete.obs");print(cor6);
cor7 <- cor(dum1,dum1,use = "complete.obs");print(cor7);cor8 <- cor(dum1,dum2,use = "complete.obs");print(cor8)

# Deteccion con coeficiente de correlacion dum2
cor1 <- cor(dum2,a1,use = "complete.obs");print(cor1);cor2 <- cor(dum2,a2,use = "complete.obs");print(cor2);
cor3 <- cor(dum2,a3,use = "complete.obs");print(cor3);cor4 <- cor(dum2,a4,use = "complete.obs");print(cor4);
cor5 <- cor(dum2,a5,use = "complete.obs");print(cor5);cor6 <- cor(dum2,a6,use = "complete.obs");print(cor6);
cor7 <- cor(dum2,dum1,use = "complete.obs");print(cor7);cor8 <- cor(dum2,dum2,use = "complete.obs");print(cor8)

# Deteccion con VIF (FIV)
library(car)
vif(m1)
vif(m2)
vif(m3)
vif(m4)
# ==> no se identifica MC fuerte

# Solucion MC: diferencias 
da1=diff(POHM) # yt - yt-1
da4=diff(EELEC)
da5=diff(INVEBRTA)
mc=lm(lb0~log(da1)+log(a2)+log(a3)+log(da4)+log(da5)+log(a6)+ita+itb+dum1+dum2)
mc=lm(dpib~diva+darancel+dtimbre)
summary(mc)
cor(diva,dtimbre)
