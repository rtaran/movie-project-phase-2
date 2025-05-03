import movie_storage
import movies

# Load movies
all_movies = movie_storage.load_movies()
print("All movies:")
for movie in all_movies:
    print(f"{movie['title']} ({movie['year']}) - Rating: {movie['rating']}")

# Test search
query = "ic"
matches = [m for m in all_movies if query in m["title"].strip().lower()]
print(f"\nSearch for '{query}':")
if matches:
    print("Matches found:")
    for m in matches:
        print(f"{m['title']} ({m['year']}) - Rating: {m['rating']}")
else:
    print("No matches found.")