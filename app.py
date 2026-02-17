from http.client import responses

import streamlit as st
import pickle
import pandas as pd
import requests     #for API
import urllib.parse
import re



def clean_title(title):
    # Remove year and extra symbols
    title = re.sub(r"\(\d{4}\)", "", title)
    title = title.replace(":", "").replace("-", "").strip()
    return title


def fetch_poster(movie_title):
    api_key = "dc0e7af0bdbd5b6262f9b27939e99c91"

    movie_title = clean_title(movie_title)
    query = urllib.parse.quote(movie_title)
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"

    response = requests.get(url)
    data = response.json()

    # Debugging: print movie title and data structure (optional)
    # print(movie_title, data)

    if "results" in data and len(data["results"]) > 0:
        first_movie = data["results"][0]
        poster_path = first_movie.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"

    # If no poster found, return a placeholder
    return "https://via.placeholder.com/500x750?text=No+Poster+Found"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movie_names.append(movie_title)
        recommended_movie_posters.append(fetch_poster(movie_title))

    return recommended_movie_names, recommended_movie_posters



movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))






st.title("Movie Recommender System🎥")
selected_movie_name = st.selectbox("🎬 Select a movie:", movies["title"].values)


if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"<p style='color:#FFD700; font-weight:bold; text-align:center;'>{names[i]}</p>",
                                unsafe_allow_html=True)
            st.image(posters[i], use_container_width=True)





