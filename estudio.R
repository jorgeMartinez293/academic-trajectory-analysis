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

biplot(PCA) # Importante lo cerca que está nota de primero y nota de segundo de bachillerato

PCA$loadings -> L
PCA$scores -> S

which.max(S[, 2]) # El segundo dato es simplemente su índice después de quitar los nulos
which.min(S[, 2])

# Regla del codo para seleccionar el número de componentes (Screen plot)
# Usaremos 'notas_novatos' sin NAs para que cor() y eigen() funcionen correctamente
plot(eigen(cor(na.omit(notas_novatos)))$values,
    type = "b",
    xlab = "Número de componente", ylab = "Valores propios",
    main = "Regla del Codo (Scree Plot)"
)
