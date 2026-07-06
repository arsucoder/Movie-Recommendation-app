# -*- coding: utf-8 -*-
"""
Netflix Style Movie Recommendation System
-----------------------------------------
Portfolio Project

Author: arsu
"""

# ==========================================================
# IMPORTS
# ==========================================================

import os
import pickle

import gdown
import pandas as pd
import streamlit as st

from styles import load_css

from utils import (
    create_lookup,
    search_movies,
    recommend,
)

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Netflix Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# LOAD CUSTOM CSS
# ==========================================================

st.markdown(
    load_css(),
    unsafe_allow_html=True,
)

# ==========================================================
# CONSTANTS
# ==========================================================

MODEL_FILE = "movie_recommendation.sav"

MOVIES_FILE = "movies.csv"

GOOGLE_DRIVE_FILE_ID = st.secrets["GOOGLE_DRIVE_FILE_ID"]

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]

DOWNLOAD_URL = (
    f"https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}"
)

# ==========================================================
# DOWNLOAD MODEL (ONLY ON FIRST RUN)
# ==========================================================

if not os.path.exists(MODEL_FILE):

    with st.spinner(
        "Downloading recommendation model..."
    ):

        gdown.download(
            DOWNLOAD_URL,
            MODEL_FILE,
            quiet=False,
        )

# ==========================================================
# LOAD MOVIES DATASET
# ==========================================================

@st.cache_data(show_spinner=False)
def load_movies():

    dataframe = pd.read_csv(MOVIES_FILE)

    dataframe.fillna("", inplace=True)

    return dataframe


# ==========================================================
# LOAD SIMILARITY MATRIX
# ==========================================================

@st.cache_resource(show_spinner=False)
def load_similarity():

    with open(MODEL_FILE, "rb") as file:

        similarity_matrix = pickle.load(file)

    return similarity_matrix


# ==========================================================
# LOAD APPLICATION DATA
# ==========================================================

movies = load_movies()

similarity = load_similarity()

lookup = create_lookup(movies)

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/7/75/Netflix_icon.svg",
        width=90,
    )

    st.markdown("## Netflix Recommender")

    st.markdown("---")

    st.success("Recommendation model loaded")

    st.markdown("### Features")

    st.markdown(
        """
- 🎬 AI Movie Recommendations
- 🔍 Search Movies
- ⭐ TMDB Ratings
- 🎭 Genres
- ⏱ Runtime
- 📅 Release Year
- 📖 Movie Overview
- ⚡ Cached TMDB API
"""
    )

    st.markdown("---")

    st.markdown("### Dataset")

    st.metric(
        "Movies",
        f"{len(movies):,}",
    )

    st.markdown("---")

    st.caption(
        "Powered by Streamlit, Scikit-Learn and TMDB"
    )


# ==========================================================
# HERO SECTION
# ==========================================================

st.markdown(
    """
<div class="hero">

<h1>🎬 Netflix Movie Recommendation System</h1>

<p>
Discover your next favorite movie with an AI-powered recommendation engine.
Search from thousands of movies and instantly receive personalized recommendations
complete with posters, ratings, genres, runtime and overview.
</p>

</div>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# SEARCH SECTION
# ==========================================================

st.markdown("## 🔍 Search Movies")

search_query = st.text_input(
    "",
    placeholder="Start typing a movie name...",
    label_visibility="collapsed",
)

selected_movie = None

if search_query:

    suggestions = search_movies(
        search_query,
        movies,
        limit=8,
    )

    if suggestions:

        selected_movie = st.selectbox(
            "",
            suggestions,
            index=0,
            label_visibility="collapsed",
        )

    else:

        st.warning("No movies found.")

# ==========================================================
# RECOMMEND BUTTON
# ==========================================================

recommend_clicked = st.button(
    "🎬 Recommend Movies",
    use_container_width=True,
    disabled=selected_movie is None,
)

st.write("")

# ==========================================================
# RECOMMENDATION ENGINE
# ==========================================================

recommendations = []

if recommend_clicked and selected_movie:

    with st.spinner("Finding similar movies..."):

        recommendations = recommend(
            movie_name=selected_movie,
            similarity=similarity,
            movies=movies,
            lookup=lookup,
            api_key=TMDB_API_KEY,
        )

# ==========================================================
# EMPTY STATE
# ==========================================================

if not recommendations:

    st.markdown("## 🍿 Welcome")

    st.write(
        """
Search for your favorite movie above and click **Recommend Movies**
to discover five similar movies complete with posters, ratings,
genres, runtime, release year, similarity score and overview.
"""
    )

    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Movies", f"{len(movies):,}")

    with c2:
        st.metric("Recommendations", "Top 5")

    with c3:
        st.metric("Search", "Instant")

    with c4:
        st.metric("TMDB", "Live")

# ==========================================================
# RESULTS HEADER
# ==========================================================

if recommendations:

    st.markdown("---")

    st.markdown(
        f"## 🎯 Because you liked **{selected_movie}**"
    )

    st.write("")

    movie_columns = st.columns(5)

# ==========================================================
# MOVIE CARDS
# ==========================================================

if recommendations:

    for column, movie in zip(movie_columns, recommendations):

        with column:

            poster = (
                movie["poster"]
                if movie["poster"]
                else "https://via.placeholder.com/500x750?text=No+Poster"
            )

            runtime = (
                f'{movie["runtime"]} min'
                if movie["runtime"]
                else "--"
            )

            genres = movie["genres"] or "Unknown"

            overview = movie["overview"] or "No overview available."

            st.markdown(
                '<div class="movie-card">',
                unsafe_allow_html=True,
            )

            st.image(
                poster,
                use_container_width=True,
            )

            st.markdown(
                f"""
<div class="movie-title">
{movie["title"]}
</div>
""",
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
<span class="badge rating">
⭐ {movie["rating"]:.1f}
</span>

<span class="badge year">
📅 {movie["year"]}
</span>

<span class="badge runtime">
⏱ {runtime}
</span>
""",
                unsafe_allow_html=True,
            )

            st.write("")

            for genre in genres.split(",")[:3]:

                st.markdown(
                    f"""
<span class="badge genre">
{genre.strip()}
</span>
""",
                    unsafe_allow_html=True,
                )

            st.write("")

            st.progress(
                min(movie["similarity"] / 100, 1.0)
            )

            st.caption(
                f"Similarity Score: {movie['similarity']}%"
            )

            with st.expander("Overview"):

                st.write(overview)

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


  # ==========================================================
# FOOTER
# ==========================================================

st.write("")
st.write("")
st.divider()

left, center, right = st.columns([2, 3, 2])

with left:

    st.markdown("### 🎬 Movie Recommendation System")

    st.caption(
        "AI-powered content recommendation using "
        "Content-Based Filtering."
    )

with center:

    st.markdown("### Tech Stack")

    st.markdown(
        """
- Streamlit
- Python
- Scikit-Learn
- Pandas
- TMDB API
- GitHub Releases
"""
    )

with right:

    st.markdown("### Features")

    st.markdown(
        """
✅ Fast Search

✅ Cached API

✅ Responsive UI

✅ Netflix Theme

✅ Similarity Score
"""
    )

st.divider()

st.markdown(
    """
<div style="text-align:center; padding:15px; color:#B3B3B3;">

Built with ❤️ using Streamlit

<br><br>

Movie Recommendation System © 2026

</div>
""",
    unsafe_allow_html=True,
)
