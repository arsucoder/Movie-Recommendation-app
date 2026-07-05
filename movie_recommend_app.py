# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 13:55:34 2026

@author: arsla
"""

import pickle
import requests
import streamlit as st

# ==========================
# Page Configuration
# ==========================
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# ==========================
# Load Saved Files
# ==========================

@st.cache_resource
def load_data():
    movies = pickle.load(open("movies.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return movies, similarity


movies, similarity = load_data()


# ==========================
# Fetch Movie Poster
# ==========================

API_KEY = "YOUR_TMDB_API_KEY"


def fetch_poster(movie_id):
    """
    Fetch movie poster from TMDB API.
    """

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    response = requests.get(url)

    data = response.json()

    poster_path = data.get("poster_path")

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path

    return None


# ==========================
# Recommendation Function
# ==========================

def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for item in movie_list:

        movie_id = movies.iloc[item[0]].movie_id

        recommended_movies.append(
            movies.iloc[item[0]].title
        )

        recommended_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, recommended_posters


# ==========================
# User Interface
# ==========================

st.title("🎬 Movie Recommendation System")

st.markdown(
    "Select your favorite movie and discover similar movies."
)

selected_movie = st.selectbox(
    "Choose a Movie",
    movies["title"].values
)


# ==========================
# Recommendation Button
# ==========================

if st.button("Recommend Movies"):

    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):

        with cols[i]:

            if posters[i]:
                st.image(posters[i])

            st.caption(names[i])