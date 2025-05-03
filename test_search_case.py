import movie_storage

# Load movies
all_movies = movie_storage.load_movies()
print("All movies:")
for movie in all_movies:
    print(f"{movie['title']} ({movie['year']}) - Rating: {movie['rating']}")

# Test search with "iC" (case-insensitive)
query = "iC"
print(f"\nSearch for '{query}':")
print(f"Query after strip().lower(): '{query.strip().lower()}'")

for movie in all_movies:
    title_lower = movie["title"].strip().lower()
    print(f"Movie: {movie['title']}, Title after strip().lower(): '{title_lower}'")
    if query.strip().lower() in title_lower:
        print(f"  Match found! '{query.strip().lower()}' is in '{title_lower}'")
    else:
        print(f"  No match. '{query.strip().lower()}' is not in '{title_lower}'")