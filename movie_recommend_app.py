import os
import pickle
import requests
import pandas as pd
import streamlit as st
import gdown

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommendation System")
st.write("Select a movie and get similar movie recommendations with posters.")

# ==========================================================
# GOOGLE DRIVE FILE DETAILS
# ==========================================================

# Replace this with your Google Drive File ID
FILE_ID = st.secrets["GOOGLE_DRIVE_FILE_ID"]

MODEL_PATH = "movie_recommendation.sav"

# Direct download link
URL = f"https://drive.google.com/uc?id={FILE_ID}"

# ==========================================================
# DOWNLOAD MODEL IF NOT PRESENT
# ==========================================================

if not os.path.exists(MODEL_PATH):
    with st.spinner("Downloading recommendation model... Please wait."):
        gdown.download(URL, MODEL_PATH, quiet=False)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_resource
def load_similarity():
    with open(MODEL_PATH, "rb") as file:
        similarity = pickle.load(file)
    return similarity


@st.cache_data
def load_movies():
    return pd.read_csv("movies.csv")


similarity = load_similarity()
movies = load_movies()

# ==========================================================
# TMDB API
# ==========================================================

# Replace with your TMDB API Key
API_KEY = st.secrets["TMDB_API_KEY"]


def fetch_poster(movie_id):
    """
    Returns poster URL using TMDB movie ID.
    """

    try:
        url = (
            f"https://api.themoviedb.org/3/movie/{movie_id}"
            f"?api_key={API_KEY}&language=en-US"
        )

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

    except Exception:
        pass

    return "https://via.placeholder.com/500x750?text=No+Poster"


# ==========================================================
# RECOMMENDATION FUNCTION
# ==========================================================

def recommend(movie_name):

    movie_index = movies[movies["title"] == movie_name].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for movie in movie_list:

        idx = movie[0]

        movie_title = movies.iloc[idx]["title"]

        movie_id = movies.iloc[idx]["id"]

        poster = fetch_poster(movie_id)

        recommended_movies.append(movie_title)

        recommended_posters.append(poster)

    return recommended_movies, recommended_posters


# ==========================================================
# UI
# ==========================================================

# ==========================================================
# UI
# ==========================================================

search_query = st.text_input(
    "🔍 Search Movie",
    placeholder="Type a movie name..."
)

selected_movie = None

if search_query:

    # Find matching movies (case-insensitive)
    filtered_movies = movies[
        movies["title"].str.contains(search_query, case=False, na=False)
    ]["title"].tolist()

    if filtered_movies:
        selected_movie = st.selectbox(
            "Select Matching Movie",
            filtered_movies
        )
    else:
        st.warning("No matching movie found.")

if st.button("Recommend Movies"):

    if selected_movie is None:
        st.error("Please search and select a movie first.")
    else:
        with st.spinner("Finding recommendations..."):

            names, posters = recommend(selected_movie)

        cols = st.columns(5)

        for i in range(5):
            with cols[i]:
                st.image(posters[i], use_container_width=True)
                st.caption(names[i])

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")
st.markdown(
    "<center>Made with ❤️ using Streamlit</center>",
    unsafe_allow_html=True
)
