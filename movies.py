import movie_storage
import matplotlib.pyplot as plt
from fuzzywuzzy import process
from colorama import Fore, Style, init
import random
import statistics
# Initialize colorama
init(autoreset=True)


def add_movie_flow():
    """Handle adding a movie."""
    title = input(Fore.BLUE + "Enter movie title: ").strip()
    if not title:
        print(Fore.RED + "Movie title cannot be empty.")
        return

    movies = movie_storage.load_movies()
    if any(m["title"].strip().lower() == title.lower() for m in movies):
        print(Fore.RED + "Movie already exists.")
        return

    try:
        rating = float(input(Fore.BLUE + "Enter movie rating (0-10): "))
        if not (0 <= rating <= 10):
            print(Fore.RED + "Rating must be between 0 and 10.")
            return
    except ValueError:
        print(Fore.RED + "Invalid rating input.")
        return

    try:
        year = int(input(Fore.BLUE + "Enter release year: "))
        if not (1800 <= year <= 2100):
            print(Fore.RED + "Please enter a valid 4-digit year between 1800 and 2100.")
            return
    except ValueError:
        print(Fore.RED + "Invalid year input.")
        return

    movie_storage.add_movie(title, rating, year)
    print(Fore.GREEN + f"Movie '{title}' added successfully!")


def delete_movie_flow():
    """Handle deleting a movie."""
    title = input(Fore.BLUE + "Enter movie title to delete: ")
    if movie_storage.delete_movie(title):
        print(Fore.GREEN + f"Movie '{title}' deleted successfully!")
    else:
        print(Fore.RED + "Movie not found.")


def update_rating_flow():
    """Handle updating a movie rating."""
    title = input(Fore.BLUE + "Enter movie title to update rating: ")
    try:
        new_rating = float(input(Fore.BLUE + "Enter new rating (0-10): "))
        if not (0 <= new_rating <= 10):
            print(Fore.RED + "Rating must be between 0 and 10.")
            return
    except ValueError:
        print(Fore.RED + "Invalid rating input.")
        return

    if update_movie_rating(title, new_rating):
        print(Fore.GREEN + f"Movie '{title}' rating updated successfully!")
    else:
        print(Fore.RED + "Movie not found.")


def show_stats_flow():
    """Handle showing movie statistics."""
    stats = get_stats()
    if stats:
        print(Fore.MAGENTA + "\nMovie Statistics:")
        print(Fore.YELLOW + f"Total Movies: {stats['total_movies']}")
        print(Fore.YELLOW + f"Average Rating: {stats['average_rating']}")
        print(Fore.YELLOW + f"Median Rating: {stats['median_rating']}")
        print(Fore.YELLOW + f"Mode Rating: {stats['mode_rating']}")
        print(Fore.YELLOW + "Highest Rated:")
        for m in stats['highest_rated']:
            print(Fore.YELLOW + f"{m['title']} ({m['rating']})")
        print(Fore.YELLOW + "Lowest Rated:")
        for m in stats['lowest_rated']:
            print(Fore.YELLOW + f"{m['title']} ({m['rating']})")
    else:
        print(Fore.RED + "No movies available.")


def exit_app():
    """Handle exiting the app."""
    print(Fore.RED + "Exiting application. Goodbye!")
    exit()


def show_menu() -> None:
    """Display the menu options."""
    print(Fore.CYAN + "\nMovie Application")
    print(Fore.YELLOW + "1. Add a movie")
    print(Fore.YELLOW + "2. Delete a movie")
    print(Fore.YELLOW + "3. Update movie rating")
    print(Fore.YELLOW + "4. Show statistics")
    print(Fore.YELLOW + "5. Search for a movie")
    print(Fore.YELLOW + "6. Show movie ratings histogram")
    print(Fore.YELLOW + "7. Pick a random movie")
    print(Fore.YELLOW + "8. List movies sorted by rating")
    print(Fore.YELLOW + "9. List all movies")
    print(Fore.RED + "10. Exit")


def search_movie() -> None:
    """Search for a movie using exact match and fuzzy fallback."""
    query = input(Fore.BLUE + "Enter the movie title: ").strip().lower()
    movies = movie_storage.load_movies()
    matches = [m for m in movies if query in m["title"].strip().lower()]

    if matches:
        print(Fore.GREEN + "Exact match(es) found:")
        for m in matches:
            print(Fore.YELLOW + f"{m['title']} ({m['year']}) - Rating: {m['rating']}")
    else:
        titles = [movie["title"] for movie in movies]
        best_match = process.extractOne(query, titles)
        if best_match and best_match[1] > 70:
            print(Fore.GREEN + f"Did you mean: {best_match[0]}?")
        else:
            print(Fore.RED + "No close matches found.")


def show_ratings_histogram() -> None:
    """Display a histogram of movie ratings."""
    movies = movie_storage.load_movies()
    ratings = [movie["rating"] for movie in movies]

    if not ratings:
        print(Fore.RED + "No movie ratings available to display.")
        return

    plt.hist(ratings, bins=10, edgecolor="black")
    plt.xlabel("Ratings")
    plt.ylabel("Number of Movies")
    plt.title("Movie Ratings Distribution")
    plt.show()


def pick_random_movie() -> None:
    """Pick and display a random movie."""
    movie = pick_random_movie_internal()
    if movie:
        print(Fore.GREEN + f"Random Pick: {movie['title']} "
                          f"({movie['year']}) - "
                          f"Rating: {movie['rating']}")
    else:
        print(Fore.RED + "No movies available.")


def list_movies_sorted() -> None:
    """List movies sorted by rating."""
    movies = get_movies_sorted_by_rating()
    if not movies:
        print(Fore.RED + "No movies available.")
        return

    print(Fore.MAGENTA + "\nMovies Sorted by Rating:")
    for movie in movies:
        print(Fore.YELLOW + f"{movie['title']} "
                           f"({movie['year']}) - "
                           f"Rating: {movie['rating']}")


def list_movies() -> None:
    """List all movies with title, year, and rating."""
    movies = movie_storage.load_movies()
    if not movies:
        print(Fore.RED + "No movies found.")
        return
    print(Fore.MAGENTA + "\nAll Movies:")
    for movie in movies:
        print(Fore.YELLOW + f"{movie['title']} "
                           f"({movie['year']}) - "
                           f"Rating: {movie['rating']}")


def update_movie_rating(title: str, new_rating: float) -> bool:
    """Update the rating of a movie."""
    movies = movie_storage.load_movies()
    updated = False
    for movie in movies:
        if movie["title"].lower() == title.lower():
            movie["rating"] = new_rating
            updated = True
            break
    if updated:
        movie_storage.save_movies(movies)
    return updated


def get_stats():
    """Calculate and return statistics about the movies."""
    movies = movie_storage.load_movies()
    if not movies:
        return None
    ratings = [movie["rating"] for movie in movies]
    total_movies = len(movies)
    average_rating = round(statistics.mean(ratings), 2)
    median_rating = round(statistics.median(ratings), 2)
    try:
        mode_rating = statistics.mode(ratings)
    except statistics.StatisticsError:
        mode_rating = "No unique mode"
    max_rating = max(ratings)
    min_rating = min(ratings)
    highest_rated = [m for m in movies if m["rating"] == max_rating]
    lowest_rated = [m for m in movies if m["rating"] == min_rating]

    return {
        "total_movies": total_movies,
        "average_rating": average_rating,
        "median_rating": median_rating,
        "mode_rating": mode_rating,
        "highest_rated": highest_rated,
        "lowest_rated": lowest_rated,
    }


def pick_random_movie_internal():
    """Return a random movie."""
    movies = movie_storage.load_movies()
    if not movies:
        return None
    return random.choice(movies)


def get_movies_sorted_by_rating():
    """Return movies sorted by rating descending."""
    movies = movie_storage.load_movies()
    return sorted(movies, key=lambda x: x["rating"], reverse=True)


def main() -> None:
    """Main application loop."""
    while True:
        show_menu()
        choice = input(Fore.CYAN + "Choose an option: ")

        dispatcher = {
            "1": add_movie_flow,
            "2": delete_movie_flow,
            "3": update_rating_flow,
            "4": show_stats_flow,
            "5": search_movie,
            "6": show_ratings_histogram,
            "7": pick_random_movie,
            "8": list_movies_sorted,
            "9": list_movies,
            "10": exit_app
        }

        action = dispatcher.get(choice)
        if action:
            action()
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
