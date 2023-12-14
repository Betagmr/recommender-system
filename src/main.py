import pickle

import requests
import streamlit as st


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_id}&api_key=8265bd1679663a7ea12ac168da84d2e8"
    data = requests.get(url).json()["results"]

    if len(data) < 1:
        return None

    poster_path = data[0]["poster_path"]
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie, n_movies=10):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1 : n_movies + 1]:
        movie_id = movies.iloc[i[0]].original_title
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


def recommend2(movie, n_movies=10):
    cluster = clusters[clusters["title"] == movie]["cluster"].values[0]
    elements = clusters[clusters["cluster"] == cluster]
    elements = elements.sort_values("rat", ascending=False)

    titles = [title for title in elements["title"]]

    recommended_movie_names = []
    recommended_movie_posters = []
    for title in titles[1:n_movies]:
        poster = fetch_poster(title)

        if poster is None:
            continue

        recommended_movie_posters.append(poster)
        recommended_movie_names.append(title)

    return recommended_movie_names, recommended_movie_posters


st.header("Movie Recommender System")
movies = pickle.load(open("movie_list.pkl", "rb"))
clusters = pickle.load(open("cluster_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movie_list = movies["title"].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button("Show Recommendation"):
    recommended_movie_names1, recommended_movie_posters1 = recommend(selected_movie)
    recommended_movie_names2, recommended_movie_posters2 = recommend2(selected_movie)

    st.title(f"Películas que se parecen a {selected_movie}")
    for index, column in enumerate(st.columns(5)):
        with column:
            st.text(recommended_movie_names1[index])
            st.image(recommended_movie_posters1[index])

    st.title(f"Otros usuarios que han visto {selected_movie} también han visto")
    for index, column in enumerate(st.columns(5)):
        with column:
            st.text(recommended_movie_names2[index])
            st.image(recommended_movie_posters2[index])
