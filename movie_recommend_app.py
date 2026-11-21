# import os
# import pickle
# import requests
# import pandas as pd
# import streamlit as st
# import gdown

# # ==========================================================
# # PAGE CONFIG
# # ==========================================================

# st.set_page_config(
#     page_title="Movie Recommendation App",
#     page_icon="🎬",
#     layout="wide"
# )

# st.title("🎬 Movie Recommendation System")
# st.write("Select a movie and get similar movie recommendations with posters.")

# # ==========================================================
# # GOOGLE DRIVE FILE DETAILS
# # ==========================================================

# # Replace this with your Google Drive File ID
# FILE_ID = st.secrets["GOOGLE_DRIVE_FILE_ID"]

# MODEL_PATH = "movie_recommendation.sav"

# # Direct download link
# URL = f"https://drive.google.com/uc?id={FILE_ID}"

# # ==========================================================
# # DOWNLOAD MODEL IF NOT PRESENT
# # ==========================================================

# if not os.path.exists(MODEL_PATH):
#     with st.spinner("Downloading recommendation model... Please wait."):
#         gdown.download(URL, MODEL_PATH, quiet=False)

# # ==========================================================
# # LOAD DATA
# # ==========================================================

# @st.cache_resource
# def load_similarity():
#     with open(MODEL_PATH, "rb") as file:
#         similarity = pickle.load(file)
#     return similarity


# @st.cache_data
# def load_movies():
#     return pd.read_csv("movies.csv")


# similarity = load_similarity()
# movies = load_movies()

# # ==========================================================
# # TMDB API
# # ==========================================================

# # Replace with your TMDB API Key
# API_KEY = st.secrets["TMDB_API_KEY"]


# def fetch_poster(movie_id):
#     """
#     Returns poster URL using TMDB movie ID.
#     """

#     try:
#         url = (
#             f"https://api.themoviedb.org/3/movie/{movie_id}"
#             f"?api_key={API_KEY}&language=en-US"
#         )

#         response = requests.get(url, timeout=10)

#         if response.status_code != 200:
#             return None

#         data = response.json()

#         poster_path = data.get("poster_path")

#         if poster_path:
#             return "https://image.tmdb.org/t/p/w500" + poster_path

#     except Exception:
#         pass

#     return "https://via.placeholder.com/500x750?text=No+Poster"


# # ==========================================================
# # RECOMMENDATION FUNCTION
# # ==========================================================

# def recommend(movie_name):

#     movie_index = movies[movies["title"] == movie_name].index[0]

#     distances = similarity[movie_index]

#     movie_list = sorted(
#         list(enumerate(distances)),
#         reverse=True,
#         key=lambda x: x[1]
#     )[1:6]

#     recommended_movies = []
#     recommended_posters = []

#     for movie in movie_list:

#         idx = movie[0]

#         movie_title = movies.iloc[idx]["title"]

#         movie_id = movies.iloc[idx]["id"]

#         poster = fetch_poster(movie_id)

#         recommended_movies.append(movie_title)

#         recommended_posters.append(poster)

#     return recommended_movies, recommended_posters


# # ==========================================================
# # UI
# # ==========================================================

# # ==========================================================
# # UI
# # ==========================================================

# search_query = st.text_input(
#     "🔍 Search Movie",
#     placeholder="Type a movie name..."
# )

# selected_movie = None

# if search_query:

#     # Find matching movies (case-insensitive)
#     filtered_movies = movies[
#         movies["title"].str.contains(search_query, case=False, na=False)
#     ]["title"].tolist()

#     if filtered_movies:
#         selected_movie = st.selectbox(
#             "Select Matching Movie",
#             filtered_movies
#         )
#     else:
#         st.warning("No matching movie found.")

# if st.button("Recommend Movies"):

#     if selected_movie is None:
#         st.error("Please search and select a movie first.")
#     else:
#         with st.spinner("Finding recommendations..."):

#             names, posters = recommend(selected_movie)

#         cols = st.columns(5)

#         for i in range(5):
#             with cols[i]:
#                 st.image(posters[i], use_container_width=True)
#                 st.caption(names[i])

# # ==========================================================
# # FOOTER
# # ==========================================================

# st.markdown("---")
# st.markdown(
#     "<center>Made with ❤️ By arsu</center>",
#     unsafe_allow_html=True
# )


import os
import pickle
import requests
import pandas as pd
import streamlit as st
import gdown

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="CineMatch | Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background: linear-gradient(135deg, #090909 0%, #151515 55%, #101010 100%);
    color: #FFFFFF;
}

/* Main content width */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Hero section */
.hero {
    text-align: center;
    padding: 45px 20px 35px 20px;
    background: linear-gradient(120deg, #1d1d1d, #292020, #151515);
    border: 1px solid #373030;
    border-radius: 20px;
    margin-bottom: 35px;
}

.hero h1 {
    font-size: 46px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 10px;
    letter-spacing: -1px;
}

.hero h1 span {
    color: #E50914;
}

.hero p {
    font-size: 17px;
    color: #BDBDBD;
    margin-bottom: 0;
}

/* Section headings */
.section-heading {
    font-size: 25px;
    font-weight: 700;
    color: #FFFFFF;
    margin-top: 25px;
    margin-bottom: 18px;
}

/* Search container */
.search-box {
    background: #1C1C1C;
    border: 1px solid #333333;
    border-radius: 16px;
    padding: 25px;
    margin-bottom: 25px;
}

/* Input fields */
.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    background-color: #252525 !important;
    color: white !important;
    border-radius: 10px !important;
}

.stTextInput label,
.stSelectbox label {
    color: #E5E5E5 !important;
    font-weight: 600 !important;
}

/* Buttons */
.stButton > button {
    background: #E50914;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 25px;
    font-size: 16px;
    font-weight: 700;
    transition: 0.3s ease;
}

.stButton > button:hover {
    background: #B80710;
    color: white;
    transform: translateY(-2px);
    border: none;
}

/* Movie cards */
.movie-card {
    background: #1C1C1C;
    border: 1px solid #333333;
    border-radius: 13px;
    padding: 12px;
    text-align: center;
    min-height: 85px;
    margin-top: 10px;
}

.movie-title {
    color: #FFFFFF;
    font-size: 15px;
    font-weight: 650;
    line-height: 1.4;
}

/* Result heading */
.result-heading {
    color: white;
    font-size: 27px;
    font-weight: 750;
    margin-top: 35px;
    margin-bottom: 5px;
}

.result-subheading {
    color: #AFAFAF;
    font-size: 14px;
    margin-bottom: 20px;
}

/* Footer */
.footer {
    text-align: center;
    color: #777777;
    padding: 30px 10px 10px 10px;
    font-size: 13px;
}

.footer span {
    color: #E50914;
    font-weight: 700;
}

/* Mobile adjustments */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 32px;
    }

    .hero p {
        font-size: 14px;
    }

    .hero {
        padding: 30px 12px;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# HERO SECTION
# ==========================================================

st.markdown("""
<div class="hero">
    <h1>🎬 Cine<span>Match</span></h1>
    <p>Discover your next favourite movie with intelligent recommendations.</p>
    <p>Find movies you'll love, based on what you already enjoy.</p>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# GOOGLE DRIVE MODEL CONFIGURATION
# ==========================================================

MODEL_PATH = "movie_recommendation.sav"

FILE_ID = st.secrets["GOOGLE_DRIVE_FILE_ID"]

URL = f"https://drive.google.com/uc?id={FILE_ID}"


# ==========================================================
# DOWNLOAD MODEL
# ==========================================================

if not os.path.exists(MODEL_PATH):

    with st.spinner("Preparing your movie recommendation engine..."):

        downloaded_file = gdown.download(
            URL,
            MODEL_PATH,
            quiet=True
        )

    if not downloaded_file or not os.path.exists(MODEL_PATH):
        st.error("Unable to download the recommendation model. Please try again later.")
        st.stop()


# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_resource
def load_similarity():

    with open(MODEL_PATH, "rb") as file:
        return pickle.load(file)


@st.cache_data
def load_movies():

    return pd.read_csv("movies.csv")


try:
    similarity = load_similarity()
    movies = load_movies()

except Exception:
    st.error("Unable to load movie data. Please check your model and CSV files.")
    st.stop()


if "title" not in movies.columns or "id" not in movies.columns:
    st.error("The movies.csv file must contain 'title' and 'id' columns.")
    st.stop()


if len(similarity) != len(movies):
    st.error("Movie data and recommendation model dimensions do not match.")
    st.stop()


# ==========================================================
# TMDB CONFIGURATION
# ==========================================================

API_KEY = st.secrets["TMDB_API_KEY"]


# ==========================================================
# FETCH MOVIE POSTER
# ==========================================================

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_poster(movie_id):

    try:

        url = (
            f"https://api.themoviedb.org/3/movie/{movie_id}"
            f"?api_key={API_KEY}&language=en-US"
        )

        response = requests.get(url, timeout=10)

        if response.status_code == 200:

            data = response.json()

            poster_path = data.get("poster_path")

            if poster_path:
                return (
                    "https://image.tmdb.org/t/p/w500"
                    + poster_path
                )

    except requests.RequestException:
        pass

    return "https://placehold.co/500x750/202020/FFFFFF?text=No+Poster"


# ==========================================================
# RECOMMENDATION ENGINE
# ==========================================================

def recommend(movie_name):

    matching_movies = movies[
        movies["title"] == movie_name
    ]

    if matching_movies.empty:
        return []

    movie_index = matching_movies.index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        enumerate(distances),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for movie in movie_list:

        idx = movie[0]

        movie_title = movies.iloc[idx]["title"]

        movie_id = movies.iloc[idx]["id"]

        poster = fetch_poster(movie_id)

        recommended_movies.append({
            "title": movie_title,
            "poster": poster
        })

    return recommended_movies


# ==========================================================
# SEARCH SECTION
# ==========================================================

st.markdown(
    '<div class="section-heading">🔍 Find Your Movie</div>',
    unsafe_allow_html=True
)

st.write(
    "Search for a movie you enjoy, select it, and let CineMatch "
    "discover similar movies for you."
)

search_query = st.text_input(
    "Search Movie",
    placeholder="Example: Avatar, Iron Man, Titanic...",
    label_visibility="collapsed"
)

selected_movie = None

if search_query:

    filtered_movies = movies[
        movies["title"].astype(str).str.contains(
            search_query,
            case=False,
            na=False,
            regex=False
        )
    ]["title"].drop_duplicates().tolist()

    if filtered_movies:

        selected_movie = st.selectbox(
            "Select your movie",
            filtered_movies,
            index=0
        )

    else:
        st.warning("No matching movies found. Try another title.")


# ==========================================================
# RECOMMENDATION BUTTON
# ==========================================================

col1, col2, col3 = st.columns([1, 1.5, 1])

with col2:

    recommend_button = st.button(
        "✨ Discover Similar Movies",
        use_container_width=True
    )


if recommend_button:

    if selected_movie is None:

        st.warning("Please search for and select a movie first.")

    else:

        with st.spinner("Finding movies you might love..."):

            try:

                recommendations = recommend(selected_movie)

                st.session_state["recommendations"] = recommendations
                st.session_state["selected_movie"] = selected_movie

            except Exception:
                st.error("Something went wrong while generating recommendations.")
                st.session_state.pop("recommendations", None)


# ==========================================================
# DISPLAY RECOMMENDATIONS
# ==========================================================

if "recommendations" in st.session_state:

    recommendations = st.session_state["recommendations"]

    selected = st.session_state["selected_movie"]

    st.markdown("---")

    st.markdown(
        '<div class="result-heading">🍿 Recommended For You</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="result-subheading">'
        f'Because you liked <b style="color:#E50914;">{selected}</b>, '
        f'here are some movies you might enjoy.'
        f'</div>',
        unsafe_allow_html=True
    )

    if recommendations:

        cols = st.columns(5, gap="medium")

        for i, movie in enumerate(recommendations):

            with cols[i]:

                st.image(
                    movie["poster"],
                    use_container_width=True
                )

                st.markdown(
                    f"""
                    <div class="movie-card">
                        <div class="movie-title">
                            {movie["title"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.info("No recommendations are available for this movie.")


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown("""
<div class="footer">
    Crafted with ❤️ by <span>arsu</span>
    <br><br>
    Powered by Streamlit & TMDB
    <br>
    © 2026 CineMatch | Movie Recommendation System
</div>
""", unsafe_allow_html=True)
