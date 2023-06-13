# Henry Labs - Machine Learning Operations (MLOps)

## Proyecto Individual: Sistema de Recomendación para Plataformas de Streaming
El objetivo del proyecto es desarrollar un sistema de recomendación de películas, basadas en similitudes con otras películas, para una start-up que provee servicios de agregación de plataformas de streaming. El proyecto se divide en varias etapas, desde el tratamiento de los datos hasta el entrenamiento del modelo de machine learning y la implementación de una API para consultar la información.

## Descripción del problema
La start-up cuenta con datos poco maduros y desorganizados, por lo tanto, se realiza un trabajo de Data Engineering para limpiar y transformar los datos, y luego crear un MVP (Minimum Viable Product) en una semana.

## Propuesta de trabajo
El proyecto se divide en las siguientes tareas:

### 1. Transformación de los datos
-    Importar el dataset 'movies_dataset.csv'  a un dataframe para:
		-   Desanidar campos anidados: "belongs_to_collection", "genres", "production_companies", "production countries", "spoken_languages" para poder unirlos al dataset y realizar consultas.
		-   Rellenar los valores nulos de los campos "revenue" y "budget" con cero.
		-   Eliminar los valores nulos del campo "release_date".
		-   Revisar que las fechas tengan el formato AAAA-mm-dd y crear una nueva columna "release_year" para extraer el año de la fecha de estreno.
		-   Crear una columna "return" que calcule el retorno de inversión dividiendo "revenue" entre "budget". Cuando no haya datos disponibles, el valor será cero.
		-   Eliminar las columnas no utilizadas: "video", "imdb_id", "adult", "original_title", "poster_path" y "homepage".

- Importar el dataset 'credits.csv' a un dataframe para:
	- Desanidar la variable 'cast'  y 'crew'
	- Eliminar las variables que no se utilizarán: 'cast', 'CastId', 'CreditId', 'Gender', 'Id', 'Order', 'ProfilePath'
	- Mantener las variables 'Director', 'Id', 'Character' y Name.

- Actualizar ambos datasets para luego unirlos por la variable en común 'Id'

- Una vez unidos, continuar con el estudio de las variables:
	- Revisar los valores con un tipo de dato diferente al que es necesario
	- Elimino las columnas que no son necesarias 
	- Acomodo los nombres de las columnas
	- Verifico los tipos de datos para acomodarlos
	- Reviso y elimino valores duplicados

### 2. Análisis exploratorio de los datos
Para investigar las relaciones entre las variables del dataset, identificar outliers o anomalías y descubrir patrones para analizar.

### 3 Desarrollo de la API
Utilizo el framework FastAPI para exponer los datos de la empresa a través de una API. Se crean 6 funciones de endpoints para consultar la información:

1.  `cantidad_filmaciones_mes(Mes)`: Devuelve la cantidad de películas estrenadas en el mes especificado.
2.  `cantidad_filmaciones_dia(Dia)`: Devuelve la cantidad de películas estrenadas en el día especificado.
3.  `score_titulo(titulo_de_la_filmación)`: Devuelve el título, año de estreno y score de una película especificada por su título.
4.  `votos_titulo(titulo_de_la_filmación)`: Devuelve el título, cantidad de votos y valor promedio de las votaciones de una película especificada por su título. Si la película no cumple con la condición de tener al menos 2000 valoraciones, se mostrará un mensaje indicando que no se cumple con esa condición.
5.  `get_actor(nombre_actor)`: Devuelve el éxito de un actor especificado por su nombre, la cantidad de películas en las que ha participado y el promedio de retorno de esas películas.
6.  `get_director(nombre_director)`: Devuelve el éxito de un director especificado por su nombre, junto con el nombre de cada película dirigida por él, su fecha de lanzamiento, retorno individual, costo y ganancia.

### 4. Sistema de recomendación
Una vez que los datos estén disponibles a través de la API y se haya realizado el análisis exploratorio, se procederá a entrenar un modelo de machine learning para crear un sistema de recomendación de películas. El sistema de recomendación se basará en la similitud de puntuación entre las películas y utilizará este criterio para recomendar películas similares a los usuarios.

El modelo de recomendación se implementará como una función adicional en la API y se llamará "recomendacion(titulo)". Esta función tomará como entrada el título de una película y devolverá una lista de Python con los nombres de las 5 películas más similares, ordenadas según el puntaje de similitud.

### 5. Deployment
Se utilizará la plataforma Render para implementar la API y permitir su consumo desde la web.


## Video de demostración
Muestra el funcionamiento de las consultas propuestas y el modelo de machine learning entrenado.