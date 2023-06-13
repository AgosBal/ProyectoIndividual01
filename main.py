import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import difflib
from fastapi import FastAPI

app = FastAPI()

movies_completo = pd.read_csv('Movies_completo.csv',parse_dates=['ReleaseDate','ReleaseYear','ReleaseMonth'])

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
    data = movies_completo

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

    num_mes = meses.get(mes.lower())

    if num_mes is None:
        raise ValueError('Dato mes inexistente')

    # Convertir la columna 'ReleaseMonth' a tipo datetime
    data['ReleaseDate'] = pd.to_datetime(data['ReleaseDate'], errors='coerce')

    filmaciones_mes = data[data['ReleaseDate'].dt.month == num_mes]

    cantidad_filmaciones = len(filmaciones_mes)

    return f"Se estrenaron {cantidad_filmaciones} filmaciones el mes {mes.capitalize()}."



@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    data = movies_completo

    dias = {
        'lunes': 0,
        'martes': 1,
        'miércoles': 2,
        'jueves': 3,
        'viernes': 4,
        'sábado': 5,
        'domingo': 6
    }

    num_dia = dias.get(dia.lower())

    if num_dia is None:
        raise ValueError('Dato día inexistente')

    filmaciones_dia = data[data['ReleaseDate'].dt.weekday == num_dia]

    cantidad_filmaciones = len(filmaciones_dia)

    return f"Se estrenaron {cantidad_filmaciones} filmaciones los días {dia.capitalize()}."




@app.get('/score_titulo/{titulo_de_la_filmacion}')
def score_titulo(titulo_de_la_filmacion: str):
    data = movies_completo

    titulo = titulo_de_la_filmacion.title()
    match = data[data['Title'] == titulo]

    if not match.empty:
        titulo1 = match['Title'].values[0]
        anio = match['ReleaseYear'].values[0]
        score_popularity = match['Popularity'].values[0]

        score_popularity = round(score_popularity, 2)
            
        return f"La película {titulo1} fue estrenada en el año {anio} con un score/popularidad de {score_popularity}."

    return "No se encontró la película especificada."

@app.get('/votos_titulo/{titulo_de_la_filmacion}')
def votos_titulo(titulo_de_la_filmacion: str):
    data = movies_completo
    data['Title'] = data['Title'].str.title()
    titulo = titulo_de_la_filmacion.title()

    if (data['Title'] == titulo).any():
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
    actor = movies_completo[movies_completo['ActorName'].apply(lambda x: isinstance(x, str) and nombre_actor in x)]
    
    if len(actor) == 0:
        return "Este integrante no se encuentra en la lista"

    qpelis = len(actor)
    retorno = actor['Return'].sum()
    promretorno = retorno / qpelis
    
    return f"El/La actor/actriz {nombre_actor} ha participado de {qpelis} filmaciones, ha conseguido un retorno de {retorno} con un promedio de {promretorno} por filmación"

@app.get('/get_director/{director}')
def get_director(director: str):
    pelis_director = []
    for index, row in movies_completo.iterrows():
        if director in row['Director']:
            pelicula = '- ' + row['Title'] + ':\n'
            if not pd.isnull(row['ReleaseDate']):
                pelicula += '  - Lanzamiento: ' + row['ReleaseDate'].strftime('%Y-%m-%d') + '\n'
            pelicula += '  - Retorno: ' + "{:.2f}".format(row['Return']) + '\n' + \
                        '  - Costo: ' + "{:.2f}".format(row['Budget']) + '\n' + \
                        '  - Ganancia: ' + "{:.2f}".format(row['Revenue']) + '\n'
            pelis_director.append(pelicula)
    
    if len(pelis_director) == 0:
        return 'No se encontraron películas para el director especificado.'

    exito = sum(row['Return'] for idx, row in movies_completo.iterrows() if director in row['Director'])
    exito = round(exito, 2)

    resultado = ['El director ' + director + ' tiene un éxito medido por retorno de ' + str(exito)]
    resultado.extend(pelis_director)

    return resultado


@app.get('/recomendacion/{titulo}')
def recomendacion(titulo: str):
    data = movies_completo

    titulo = titulo.title()

    palabras_clave = set(titulo.split())

    peliculas_similares = data[data['Title'].apply(lambda x: any(word in x for word in palabras_clave))]
    peliculas_similares = peliculas_similares[peliculas_similares['Title'] != titulo]
    peliculas_similares = peliculas_similares.sort_values(by='Popularity', ascending=False)
    peliculas_recomendadas = peliculas_similares.head(5)
    lista_recomendada = peliculas_recomendadas['Title'].tolist()

    return {'Lista recomendada': lista_recomendada}
