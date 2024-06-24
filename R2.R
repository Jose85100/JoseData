# Instalamos los paquetes
install.packages("tidyverse")
install.packages("tokenizers")

library(tidyverse)
library(tokenizers)

texto <- paste("También entiendo que como es temporada de elecciones, 
las expectativas para lo que lograremos este año son bajas. 
Aún así, señor Presidente de la Cámara de Representantes, 
aprecio el enfoque constructivo que usted y los otros líderes adoptaron 
a finales del año pasado para aprobar un presupuesto, 
y hacer permanentes los recortes de impuestos para las 
familias trabajadoras. Así que espero que este año podamos trabajar 
juntos en prioridades bipartidistas como la reforma de la justicia penal 
y ayudar a la gente que está luchando contra la adicción a fármacos 
de prescripción. Tal vez podamos sorprender de nuevo a los cínicos.")

# Dividir el texto en palabras individuales.
palabras <- tokenize_words(texto)

#Ha eliminado todos los signos de puntuación, 
#ha dividido el texto en palabras individuales 
#y ha convertido todo a minúsculas
palabras

# Longitud
length(palabras)
length(palabras[[1]])
class(palabras)

tabla <- table(palabras[[1]])
tabla <- data.frame(palabra = names(tabla), recuento = as.numeric(tabla))
tabla

arrange(tabla, desc(recuento))

# Dividir el texto en oraciones individuales.
oraciones <- tokenize_sentences(texto)
oraciones

oraciones_palabras <- tokenize_words(oraciones[[1]])
oraciones_palabras
length(oraciones_palabras)

length(oraciones_palabras[[1]])
length(oraciones_palabras[[2]])
length(oraciones_palabras[[3]])
length(oraciones_palabras[[4]])

sapply(oraciones_palabras, length)

# ANALISIS DEL DISCURSO DE BARACK OBAMA 2016 EN LA UNION
base_url <- "https://programminghistorian.org/assets/basic-text-processing-in-r"
url <- sprintf("%s/sotu_text/236.txt", base_url)
texto <- paste(readLines(url), collapse = "\n")

palabras <- tokenize_words(texto)
length(palabras[[1]])

tabla <- table(palabras[[1]])
tabla <- data.frame(word = names(tabla), count = as.numeric(tabla))
tabla <- arrange(tabla, desc(count))
tabla

palabras_frecuentes <- read_csv(sprintf("%s/%s", base_url, "word_frequency.csv"))
palabras_frecuentes

tabla <- inner_join(tabla, palabras_frecuentes)
tabla

filter(tabla, frequency < 0.1)

head(filter(tabla, frequency < 0.002),15)

# DISCURSO PRESIDENTES USA
metadatos <- read_csv(sprintf("%s/%s", base_url, "metadata.csv"))
metadatos

tabla <- filter(tabla, frequency < 0.002)
resultado <- c(metadatos$president[236], metadatos$year[236], tabla$word[1:5])
paste(resultado, collapse = "; ")

C:\\Users\Martha Corrales\\Documents\\Maestria Mat Aplicada\\Sabado7\\sotu_text

input_loc <-"C:\\Users\\Martha Corrales\\Documents\\Maestria Mat Aplicada\\Sabado7\\sotu_text"
archivos <- dir(input_loc, full.names = TRUE)
texto <- c()
for (f in archivos) {
texto <- c(texto, paste(readLines(f), collapse = "\n"))
}

palabras <- tokenize_words(texto)
sapply(palabras, length)


qplot(metadatos$year, sapply(palabras, length)) + labs(x = "Año", y = "Número de palabras")

qplot(metadatos$year, sapply(palabras, length), color = metadatos$sotu_type) + labs(x = "Año", y = "Número de palabras", color = "Modalidad del discurso")

oraciones <- tokenize_sentences(texto)
oraciones_palabras <- sapply(oraciones, tokenize_words)

longitud_oraciones <- list()
for (i in 1:nrow(metadatos)) {
longitud_oraciones[[i]] <- sapply(oraciones_palabras[[i]], length)
}

media_longitud_oraciones <- sapply(longitud_oraciones, median)

qplot(metadatos$year, media_longitud_oraciones) + labs(x = "Año", y = "Longitud media de las oraciones")
qplot(metadatos$year, media_longitud_oraciones) + geom_smooth() + labs(x = "Año", y = "Longitud media de las oraciones")

descripcion <- c()
for (i in 1:length(palabras)) {
  tabla <- table(palabras[[i]])
  tabla <- data_frame(word = names(tabla), count = as.numeric(tabla))
  tabla <- arrange(tabla, desc(count))
  tabla <- inner_join(tabla, palabras_frecuentes)
  tabla <- filter(tabla, frequency < 0.002)
  resultado <- c(metadatos$president[i], metadatos$year[i], tabla$word[1:5])
  descripcion <- c(descripcion, paste(resultado, collapse = "; "))
}

class(descripcion)
metadatos$president
