import requests
import streamlit as st

# -------------------------------------------------------
# Fast Movie Lookup Dictionary
# -------------------------------------------------------

@st.cache_resource
def create_lookup(movies):
    """
    Creates a dictionary for O(1) movie lookup.
    """
    return {
        title.lower(): idx
        for idx, title in enumerate(movies["title"])
    }


# -------------------------------------------------------
# Search Suggestions
# -------------------------------------------------------

def search_movies(query, movies, limit=8):

    if not query:
        return []

    query = query.lower().strip()

    results = movies[
        movies["title"]
        .str.lower()
        .str.contains(query, na=False)
    ]

    return results["title"].tolist()[:limit]


# -------------------------------------------------------
# Parse Genres
# -------------------------------------------------------

def parse_genres(text):

    if not isinstance(text, str):
        return "Unknown"

    text = text.replace("|", ", ")

    return text


# -------------------------------------------------------
# Extract Release Year
# -------------------------------------------------------

def release_year(date):

    if not isinstance(date, str):
        return "----"

    return date[:4]


# -------------------------------------------------------
# TMDB DETAILS
# -------------------------------------------------------

@st.cache_data(ttl=86400)
def fetch_movie_details(movie_id, api_key):

    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}"
        f"?api_key={api_key}"
        "&language=en-US"
    )

    try:

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return {}

        data = response.json()

        return {

            "poster":
                "https://image.tmdb.org/t/p/w500"
                + data["poster_path"]
                if data.get("poster_path")
                else None,

            "overview":
                data.get("overview", ""),

            "rating":
                data.get("vote_average", 0),

            "runtime":
                data.get("runtime", 0),

            "genres":
                ", ".join(
                    [g["name"] for g in data.get("genres", [])]
                )
        }

    except Exception:

        return {}


# -------------------------------------------------------
# Recommendation Engine
# -------------------------------------------------------

def recommend(movie_name,
              similarity,
              movies,
              lookup,
              api_key):

    movie_index = lookup.get(movie_name.lower())

    if movie_index is None:
        return []

    distances = similarity[movie_index]

    recommendations = sorted(

        list(enumerate(distances)),

        key=lambda x: x[1],

        reverse=True

    )[1:6]

    result = []

    for idx, score in recommendations:

        movie = movies.iloc[idx]

        details = fetch_movie_details(
            movie["id"],
            api_key
        )

        result.append({

            "title": movie["title"],

            "poster": details.get("poster"),

            "rating": details.get(
                "rating",
                movie.get("vote_average", 0)
            ),

            "overview": details.get(
                "overview",
                movie.get("overview", "")
            ),

            "runtime": details.get(
                "runtime",
                movie.get("runtime", 0)
            ),

            "genres": details.get(
                "genres",
                parse_genres(movie["genres"])
            ),

            "year": release_year(
                movie["release_date"]
            ),

            "similarity": round(score * 100, 1)
        })

    return result

                  
