import pandas as pd


# Crear el DataFrame "pelis"
data=pd.read_csv("prueba2.csv")
# data.to_excel("databases/data.xlsx",index=False)
pelis = pd.DataFrame(data)

# Convertir las columnas de géneros a float
genres = pelis.columns[1:]
pelis[genres] = pelis[genres].astype(float)

# Elegir 5 películas random
random_movies = pelis.sample(10)

# Pedir al usuario que puntúe las películas
ratings = []
for movie in random_movies["Película"]:
    rating = int(input(f"Puntúa la película '{movie}' del 0 al 10: "))
    ratings.append(rating)

# Crear el DataFrame "datosUsuario" con películas en las filas y géneros como columnas
datosUsuario = pd.DataFrame(0, index=random_movies["Película"], columns=pelis.columns[1:])
for i, movie in enumerate(random_movies["Película"]):
    genres = pelis[pelis["Película"] == movie].iloc[0, 1:]
    for genre in genres.index:
        if genres[genre] == 1:
            datosUsuario.loc[movie, genre] = ratings[i]
# datosUsuario.to_csv("databases/datoUsuario.csv",index=False)
# datosUsuario.to_excel("databases/datoUsuario.xlsx",index=False)
# Sumar los puntajes por género
genre_sums = datosUsuario.sum(axis=0)

# Dividir cada puntaje por género por la cantidad de películas en "pelis"
total_movies = len(pelis)
average_ratings = genre_sums / total_movies

for genre in average_ratings.index:
    pelis.loc[pelis[genre] == 1, genre] = average_ratings[genre]
# pelis.to_excel("databases/pelis.xlsx",index=False)
# pelis.to_csv("databases/pelis.csv",index=False)

# Sumar los puntajes de sus géneros y obtener resultado final
pelis["Puntaje Total"] = pelis.iloc[:, 1:].sum(axis=1)
# pelis.to_excel("databases/pelis_2.xlsx",index=False)
# pelis.to_csv("databases/pelis_2.csv",index=False)

# Devolver los títulos de las tres películas con mayor puntaje
top_3_movies = pelis.nlargest(3, "Puntaje Total")["Película"]

print("Las tres películas con mayor puntaje son:")
for movie in top_3_movies:
    print(movie)