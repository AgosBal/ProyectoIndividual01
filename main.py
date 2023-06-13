#Importo librerías
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import difflib
from fastapi import FastAPI

#Instancia FastAPI
app = FastAPI()


#Importo los datos necesarios
movies_completo = pd.read_csv('Datasets\Movies_completo.csv',parse_dates=['ReleaseDate','ReleaseYear','ReleaseMonth'])


#---------- Queries-----
@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
    '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes historicamente'''
    data = movies_completo
    
    #Defino el diccionario 'meses' donde figuran los nombres de los meses en español
    meses = {
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'octubre': 10,
        'noviembre': 11,
        'diciembre': 12
    }

    #Obtengo el número de meses que coinciden con el mes ingresado, ignorando mayúsculas y minúsculas
    num_mes = meses.get(mes.lower())

    if num_mes is None:
        raise ValueError('Dato mes inexistente')

    # Convertir la columna 'ReleaseMonth' a tipo datetime
    data['ReleaseDate'] = pd.to_datetime(data['ReleaseDate'], errors='coerce')

    #Utilizo la columna 'ReleaseDate' para obtener el mes de las películas y compara con el valor 'num_mes'
    filmaciones_mes = data[data['ReleaseDate'].dt.month == num_mes]

    #Cuento el número de filas en 'filmaciones_mes'
    cantidad_filmaciones = len(filmaciones_mes)

    return f"Se estrenaron {cantidad_filmaciones} filmaciones el mes {mes.capitalize()}."



@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrebaron ese dia historicamente'''
    data = movies_completo

    #Defino el diccionario 'días' donde figuran los nombres de los días de la semana en español
    dias = {
        'lunes': 0,
        'martes': 1,
        'miércoles': 2,
        'jueves': 3,
        'viernes': 4,
        'sábado': 5,
        'domingo': 6
    }
    
    #Obtengo el número de días de la semana que coinciden con el día ingresado
    num_dia = dias.get(dia.lower())
    
    if num_dia is None:
        raise ValueError('Dato día inexistente')

    #Utilizo la columna 'ReleaseDate' para obtener el dia de la semana de las películas y compara con el valor 'num_dia'
    filmaciones_dia = data[data['ReleaseDate'].dt.weekday == num_dia]
    
    #Cuento el número de filas en 'filmaciones_dia'
    cantidad_filmaciones = len(filmaciones_dia)

    return f"Se estrenaron {cantidad_filmaciones} filmaciones los días {dia.capitalize()}."



@app.get('/score_titulo/{titulo_de_la_filmacion}')
def score_titulo(titulo_de_la_filmacion: str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score'''
    data = movies_completo

    #Convierto el título ingresado a formato título, capitalizando la primera letra de cada palabra
    titulo = titulo_de_la_filmacion.title()
    
    #Busco coincidencia en data dónde el título de la película sea igual a 'título'
    match = data[data['Title'] == titulo]

    #Si match no está vacío, se encontró una coincidencia y extrae título, año de estreno y score 
    if not match.empty:
        titulo1 = match['Title'].values[0]
        anio = match['ReleaseYear'].values[0]
        score_popularity = match['Popularity'].values[0]

        score_popularity = round(score_popularity, 2)
            
        return f"La película {titulo1} fue estrenada en el año {anio} con un score/popularidad de {score_popularity}."

    return "No se encontró la película especificada."




@app.get('/votos_titulo/{titulo_de_la_filmacion}')
def votos_titulo(titulo_de_la_filmacion: str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. 
    La misma variable deberá de contar con al menos 2000 valoraciones, caso contrario, debemos contar con un mensaje avisando que no cumple
    esta condición y que por ende, no se devuelve ningun valor.'''
    
    data = movies_completo
    
    #Capitalizo la primera letra de cada palabra de la columna 'Title' y luego el 'titulo_de_la_filmacion' para que sea insensible a mayúsculas y minúsculas
    data['Title'] = data['Title'].str.title()
    titulo = titulo_de_la_filmacion.title()

    #Verifico si hay coincidencia en 'data' entre el título ingresado y los datos de la columna 'Title'
    if (data['Title'] == titulo).any():
        #Verifico el requisito de la cantidad de votos
        if data[data['Title'] == titulo]['VoteCount'].item() < 2000:
            return "La película no cuenta con al menos 2000 valoraciones."
        else:
            anio = data[data['Title'] == titulo]['ReleaseYear'].item()
            qvotos = data[data['Title'] == titulo]['VoteCount'].item()
            promedio = data[data['Title'] == titulo]['VoteAverage'].item()

            qvotos = int(qvotos)

            return f"La película {titulo} fue estrenada en el año {anio}. La misma cuenta con un total de {qvotos} valoraciones, con un promedio de {promedio}."
    else:
        return "La película no se encontró."
    

    
@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor: str):
    '''Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, la cantidad de películas que en las que ha participado y el promedio de retorno'''
    
    #Busco en el dataframe las filas que contienen el nombre del actor
    actor = movies_completo[movies_completo['ActorName'].apply(lambda x: isinstance(x, str) and nombre_actor in x)]
    
    if len(actor) == 0:
        return "Este integrante no se encuentra en la lista"

    qpelis = len(actor)
    retorno = actor['Return'].sum()
    promretorno = retorno / qpelis
    
    return f"El/La actor/actriz {nombre_actor} ha participado de {qpelis} filmaciones, ha conseguido un retorno de {retorno} con un promedio de {promretorno} por filmación"



@app.get('/get_director/{director}')
def get_director(director: str):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.'''
    
    #Creo la lista en la que se guardan los detalles de la película dirigida por el 'director'
    pelis_director = []
    for index, row in movies_completo.iterrows():
        if director in row['Director']:
            #Creo una cadena de texto que contiene los detalles de la película
            pelicula = '- ' + row['Title'] + ':\n'
            #Si la fecha de lanzamiento no es nula se agrega una línea adicional a la cadena 'película'
            if not pd.isnull(row['ReleaseDate']):
                pelicula += '  - Lanzamiento: ' + row['ReleaseDate'].strftime('%Y-%m-%d') + '\n'
            pelicula += '  - Retorno: ' + "{:.2f}".format(row['Return']) + '\n' + \
                        '  - Costo: ' + "{:.2f}".format(row['Budget']) + '\n' + \
                        '  - Ganancia: ' + "{:.2f}".format(row['Revenue']) + '\n'
            pelis_director.append(pelicula.replace('\n',''))
    
    if len(pelis_director) == 0:
        return 'No se encontraron películas para el director especificado.'

    exito = sum(row['Return'] for idx, row in movies_completo.iterrows() if director in row['Director'])
    exito = round(exito, 2)

    resultado = ['El director ' + director + ' tiene un éxito medido por retorno de ' + str(exito)]
    resultado.extend(pelis_director)

    return resultado


@app.get('/recomendacion/{titulo}')
def recomendacion(titulo: str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    data = movies_completo

    #Convierto el título ingresado para que cada palabra tenga primera letra mayúscula
    titulo = titulo.title()

    #Creo un conjunto de palabras claves a partir del título de la película.
    palabras_clave = set(titulo.split())

    #Filtro las películas en 'data' con al menos una de las palabras clave en el título. 
    peliculas_similares = data[data['Title'].apply(lambda x: any(word in x for word in palabras_clave))]
    
    #Elimino las películas con el mismo título
    peliculas_similares = peliculas_similares[peliculas_similares['Title'] != titulo]
    
    #Ordeno las películas obtenidas por valores 'Popularity'
    peliculas_similares = peliculas_similares.sort_values(by='Popularity', ascending=False)
    
    #Selecciono las 5 primeras películas
    peliculas_recomendadas = peliculas_similares.head(5)
    
    #Con los títulos creo una lista
    lista_recomendada = peliculas_recomendadas['Title'].tolist()

    return {'Lista recomendada': lista_recomendada}

