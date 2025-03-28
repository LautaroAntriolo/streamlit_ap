import pandas as pd
import streamlit as st
# color azul #1E70B0
# Carga de datos
peliculas = pd.read_csv("data_peliculas.csv")

st.title(":blue[Selector de películas de AP!]")
st.title("Seleccioná diez películas que hayas visto y calificalas según cuánto te gustaron:")

peliculas_vistas = st.multiselect(":blue[Películas vistas:]", list(peliculas['title']))
nombre_pelis_lista = peliculas_vistas

calificacion_peli_lista = []
for pelicula in peliculas_vistas:
    calificaciones = st.slider(f"Calificá la peli {pelicula}:", 1  , 10)
    calificacion_peli_lista.append(calificaciones)

# Buscando películas
if st.button(":blue[Enviar]"):
    if len(peliculas_vistas) == 0:
        st.error("Debe seleccionar diez películas.")
    else:
        # Crear el DataFrame "datosUsuario" con películas en las filas y géneros como columnas
        datosUsuario = pd.DataFrame(0, index=nombre_pelis_lista, columns=peliculas.columns[1:])
        
        for i, movie in enumerate(nombre_pelis_lista):
            generos = peliculas[peliculas["title"] == movie].iloc[0, 1:]
            for genero in generos.index:
                if generos[genero] == 1:
                    datosUsuario.loc[movie, genero] = calificacion_peli_lista[i]

        # Sumar los puntajes por género
        genre_sums = datosUsuario.sum(axis=0)

        # Dividir cada puntaje por género por la cantidad de películas en "pelis"
        total_movies = len(peliculas)
        average_ratings = genre_sums / total_movies

        for genre in average_ratings.index:
            peliculas.loc[peliculas[genre] == 1, genre] = average_ratings[genre]
        
        # Sumar los puntajes de sus géneros y obtener resultado final
        peliculas["Puntaje Total"] = peliculas.iloc[:, 1:].sum(axis=1)

        # Devolver los títulos de las tres películas con mayor puntaje
        top_3_movies = peliculas.sort_values(by="Puntaje Total", ascending=False)["title"][:3]
        
        st.title(":blue[De acuerdo a tus puntuaciones, AP te recomienda:]")
        for movie in top_3_movies:
            st.write("👉", movie)
