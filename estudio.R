d <- read.csv("./specifics/media_alumnos.csv", sep = ",")
notas <- d[, 2:7]
novatos <- read.csv("./specifics/media_alumnos_filtrado.csv", sep = ",")
notas_novatos <- novatos[, 2:7]

# Primero, observemos la tasa de abandono escolar
abandono <- colMeans(is.na(notas_novatos)) * 100
plot(abandono, type = "l")

# Ahora, veamos la distribución de las notas por año
boxplot(notas, names = colnames(notas), main = "Distribución de Notas por Año", ylab = "Nota") # Vemos que siguen una distribución normal

# Media y desviación típica por año
media_por_ano <- colMeans(notas, na.rm = TRUE)
sd_por_ano <- sapply(notas, sd, na.rm = TRUE)
print(media_por_ano)
print(sd_por_ano)

# Media y desviación típica general (todos los años combinados)
notas_vector <- unlist(notas, use.names = FALSE)
notas_vector <- notas_vector[!is.na(notas_vector)]
media_general <- mean(notas_vector)
sd_general <- sd(notas_vector)
cat("Media general:", media_general, "\n")
cat("Desviación típica general:", sd_general, "\n")

# Test de normalidad de Shapiro-Wilk general
shapiro.test(notas_vector) # No se puede porque es una muestra demasiado grande

# Test de normalidad de Shapiro-Wilk para cada año
shapiro.test(notas$media_1E[!is.na(notas$media_1E)])
shapiro.test(notas$media_2E[!is.na(notas$media_2E)])
shapiro.test(notas$media_3E[!is.na(notas$media_3E)])
shapiro.test(notas$media_4E[!is.na(notas$media_4E)])
shapiro.test(notas$media_1B[!is.na(notas$media_1B)])
shapiro.test(notas$media_2B[!is.na(notas$media_2B)])
# Se observa un p-valor casi nulo en todos los casos, luego siguen una distribucion normal

# Gráfica de densidades superpuestas por año
anos <- colnames(notas)
colores <- rainbow(length(anos))

# Calcular densidades (ignorando NAs) para definir los límites de los ejes
densidades <- lapply(anos, function(col) density(notas[[col]], na.rm = TRUE))
x_range <- range(sapply(densidades, function(d) range(d$x)))
y_range <- c(0, max(sapply(densidades, function(d) max(d$y))) * 1.1)

plot(NULL,
    xlim = x_range, ylim = y_range,
    main = "Distribución de Densidad de Notas por Año",
    xlab = "Nota media", ylab = "Densidad"
)

for (i in seq_along(anos)) {
    lines(densidades[[i]], col = colores[i], lwd = 2)
}

legend("topright", legend = anos, col = colores, lwd = 2, bty = "n")

# Podemos observar que, claramente, la nota de un alumno está muy relacionada con sus notas previas
plot(notas)

# Concretamente, obtenemos la siguiente matriz de correlación:
correlacion_medias <- cor(notas, use = "complete.obs")
print(correlacion_medias)

#######################################
# Análisis de componentes principales #
#######################################

PCA <- princomp(na.omit(notas_novatos, cor = TRUE))
summary(PCA, loadings = TRUE)

# Aunque ya lo hemos visto en el summary, observamos gráficamente como debemos usar 2 componentes principales
plot(eigen(cor(na.omit(notas_novatos)))$values,
     type = "b",
     xlab = "Número de componente", ylab = "Valores propios",
     main = "Regla del Codo"
)

biplot(PCA) # Importante lo cerca que está nota de primero y nota de segundo de bachillerato, INTERPRETALO

PCA$loadings -> L
L # Viendo los loadings, podemos observar que la primera componente nos dice que tan buenos estudiantes son en general.
# Y la segunda componente nos indica la diferencia que ha habido entre cuando llegaron al instituto y cuando salieron (ya que es negativo en los últimos cursos)
PCA$scores -> S
S

which.max(S[, 2]) # El segundo dato es simplemente su índice después de quitar los nulos
which.min(S[, 2])

SAT<-cor(na.omit(notas_novatos),S)
SAT # Destaca la buenísima saturación que hay en la componente 1
COM2<-SAT[,1]**2 + SAT[,2]**2 # Comunalidad
COM2 # Vemos que las notas están muy bien representadas en general.

####################
# Análisis cluster #
####################

# No sería necesario estandarizar, ya que de por sí las notas están en la misma escala (0-10)
# Pero lo hacemos por si acaso, para que no haya ningún tipo de sesgo

ds <- as.data.frame(scale(na.omit(notas_novatos)))
plot(ds, pch=20)

library(NbClust)
NbClust(ds,method='complete',index='all')$Best.nc # nos dicen que debemos usar dos grupos

set.seed(1234) # Establecemos una semilla para la reproducibilidad
CA <- kmeans(ds, centers = 2, nstart = 25)
CA

# Guardamos los centroides
C1<-CA$centers[1,]
C2<-CA$centers[2,]

# Creemos un dataframe con el grupo al que pertenecen incluido
Y<-CA$cluster
d1<-data.frame(na.omit(notas_novatos),Y)
View(d1)

library(cluster)
clusplot(ds,CA$cluster,color=T,shade=T,labels=2,cex=0.5,lines=0)
# Puesto que los grupos no son especialmente influenciados por la segunda componente 
# principal, podemos interpretar que lo que nos separa es según la componente 1 principalmente,
# que hemos comprobado antes que es que tan buen estudiante son, luego podemos interpretar
# que los dos grupos que ha creado sería algo así como buenos y malos estudiantes

CA$withinss # El segundo grupo está algo más disperso, también se puede observar en el gráfico

# Concretamente, hemos obtenido una disminución del 0.57%
1 - (CA$tot.withinss/CA$totss) # No hemos obtenido una disminución increíble, pero si aceptable.



