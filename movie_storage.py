import json
from typing import Optional, Dict, List, Union

MOVIES_FILE = "data.json"

def load_movies() -> List[Dict[str, Union[str, int, float]]]:
    """Load movies from the JSON file."""
    try:
        with open(MOVIES_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("movies", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_movies(movies: List[Dict[str, Union[str, int, float]]]) -> None:
    """Save movies to the JSON file."""
    with open(MOVIES_FILE, "w", encoding="utf-8") as file:
        json.dump({"movies": movies}, file, indent=4)

def add_movie(title: str, rating: float, year: int) -> None:
    """Add a new movie to the database."""
    movies = load_movies()
    movies.append({"title": title, "rating": rating, "year": year})
    save_movies(movies)

def delete_movie(title: str) -> bool:
    """Delete a movie by title."""
    movies = load_movies()
    updated_movies = [m for m in movies if m["title"].lower() != title.lower()]

    if len(updated_movies) == len(movies):
        return False  # Movie not found

    save_movies(updated_movies)
    return True  # Movie deleted