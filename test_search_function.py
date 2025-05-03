import movie_storage
from fuzzywuzzy import process
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def search_movie_test():
    """Test the search_movie function."""
    query = "iC"
    print(f"Query: '{query}'")
    
    movies = movie_storage.load_movies()
    matches = [m for m in movies if query.strip().lower() in m["title"].strip().lower()]
    
    print(f"Matches found: {len(matches)}")
    for m in matches:
        print(f"Match: {m['title']}")
    
    if matches:
        print("Exact match(es) found:")
        for m in matches:
            print(f"{m['title']} ({m['year']}) - Rating: {m['rating']}")
    else:
        titles = [movie["title"] for movie in movies]
        best_match = process.extractOne(query, titles)
        print(f"Best match: {best_match}")
        if best_match and best_match[1] > 70:
            print(f"Did you mean: {best_match[0]}?")
        else:
            print("No close matches found.")

# Run the test
search_movie_test()