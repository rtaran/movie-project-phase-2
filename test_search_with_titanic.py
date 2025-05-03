import movie_storage

# Add Titanic to the list of movies
movies = movie_storage.load_movies()
movies.append({"title": "Titanic", "rating": 8.0, "year": 1997})
movie_storage.save_movies(movies)

# Load movies again to verify Titanic was added
all_movies = movie_storage.load_movies()
print("All movies:")
for movie in all_movies:
    print(f"{movie['title']} ({movie['year']}) - Rating: {movie['rating']}")

# Test search with "ic"
query = "ic"
matches = [m for m in all_movies if query in m["title"].strip().lower()]
print(f"\nSearch for '{query}':")
if matches:
    print("Matches found:")
    for m in matches:
        print(f"{m['title']} ({m['year']}) - Rating: {m['rating']}")
else:
    print("No matches found.")

# Test search with "iC" (case-insensitive)
query = "iC"
matches = [m for m in all_movies if query.lower() in m["title"].strip().lower()]
print(f"\nSearch for '{query}':")
if matches:
    print("Matches found:")
    for m in matches:
        print(f"{m['title']} ({m['year']}) - Rating: {m['rating']}")
else:
    print("No matches found.")