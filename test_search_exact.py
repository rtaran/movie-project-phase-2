import movie_storage
from fuzzywuzzy import process
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def search_movie_test():
    """Test the search_movie function with the exact same code as in movies.py."""
    query = "iC".strip().lower()
    print(f"Query: '{query}'")
    movies = movie_storage.load_movies()
    matches = [m for m in movies if query in m["title"].strip().lower()]
    print(f"Matches found: {len(matches)}")
    for m in matches:
        print(f"Match: {m['title']}")

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

# Run the test
search_movie_test()
