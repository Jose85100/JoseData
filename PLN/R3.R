# Instalar las libreria
install.packages("tm")  # mineri­a de texto
install.packages("SnowballC") # text stemming (ingles)
install.packages("wordcloud") # nube de palabras
install.packages("RColorBrewer") # paletas de colores

# Se cargan las libreria
library("tm")
library("SnowballC")
library("wordcloud")
library("RColorBrewer")

# Lectura del texto
text <- readLines('ensayo6.txt')
docs <- Corpus(VectorSource(text))
inspect(docs)

# Una vez cargado el texto, debe limpiarse.
#quitar caractees especiales
toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
docs <- tm_map(docs, toSpace, "/")
docs <- tm_map(docs, toSpace, "@")
docs <- tm_map(docs, toSpace, "\\|")

#limpiar texto
# minusculas
docs <- tm_map(docs, content_transformer(tolower))
# Sin numeros
docs <- tm_map(docs, removeNumbers)
# Sin puntuacion
docs <- tm_map(docs, removePunctuation)
# Espacios en blanco
docs <- tm_map(docs, stripWhitespace)

#Remove spanish common stopwords
docs <- tm_map(docs, removeWords, stopwords("spanish"))
# Remove your own stop word
# specify your stopwords as a character vector
#docs <- tm_map(docs, removeWords, c("blabla1", "blabla2")) 
# Text stemming in english
#docs <- tm_map(docs, stemDocument)


#Con el texto preparado, es hora de convertirlo en una matriz. 
#El procedimiento es similar al que se realiza cuando se obtienen variables "dummy".
dtm <- TermDocumentMatrix(docs)


# Sobre este objeto, ya es posible realizar las primeras 
# exploraciones del texto: busqueda de terminos frecuentes y correlaciones.
findFreqTerms(dtm, lowfreq = 20)
findAssocs(dtm, terms="amor", corlimit = 0.2)


#Sim embargo, aun esta la duda sobre dtm, asi­ que la transformaremos para entender dicho objeto.
m <- as.matrix(dtm)

m1<-as.data.frame(m)
library(FactoMineR)
ac <-CA(m1)

#Finalmente, esa matriz dara paso a un DF, necesario para nuestro diagrama.
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
head(d, 20)


# Una vez creado el DF, se puede describir su contenido.

barplot(d[1:20,]$freq, las = 2, names.arg = d[1:20,]$word,
        col ="lightblue", main ="Palabras frecuentes",
        ylab = "Frecuencia")

# Vemos que la palabra "que" aparece muchas veces, esto es de esperarse, por su frecuencia de uso en español. Finalmente veamos la nube de palabras.
set.seed(1234)
wordcloud(words = d$word, freq = d$freq, min.freq = 12,
          max.words=200, random.order=FALSE, rot.per=0.35, 
          colors=brewer.pal(12, "Paired"))


# Finalmente, usaremos las herramientas de anÃ¡lisis sobre el texto.
findFreqTerms(dtm, lowfreq = 3)
findAssocs(dtm, terms="plataforma", corlimit = 0.2)
findAssocs(dtm, terms="problema", corlimit = 0.2)
findAssocs(dtm, terms="solo", corlimit = 0.2)

