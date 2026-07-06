import pandas as pd

def search_movies(query, movies):

    if len(query) < 2:
        return []

    query = query.lower()

    results = movies[
        movies["title"].str.lower().str.contains(query, na=False)
    ]

    return results["title"].head(8).tolist()
