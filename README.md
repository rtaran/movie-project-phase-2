# Movie Database Application

A command-line application for managing a personal movie database. This application allows users to add, delete, update, search, and view statistics about their movie collection.

## Features

- Add movies with title, rating, and release year
- Delete movies by title
- Update movie ratings
- Search for movies (with partial matching and fuzzy search fallback)
- Display movie statistics (average rating, highest/lowest rated movies, etc.)
- Generate a histogram of movie ratings
- Pick a random movie from your collection
- List movies sorted by rating
- List all movies in the database

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Dependencies

- colorama: For colored terminal output
- matplotlib: For generating histograms
- fuzzywuzzy: For fuzzy string matching in search

## Usage

Run the application with:

```
python movies.py
```

### Menu Options

1. **Add a movie**: Add a new movie to the database with title, rating, and release year.
2. **Delete a movie**: Remove a movie from the database by title.
3. **Update movie rating**: Change the rating of an existing movie.
4. **Show statistics**: Display statistics about your movie collection.
5. **Search for a movie**: Find movies by title (supports partial matching).
6. **Show movie ratings histogram**: Generate a visual representation of your ratings distribution.
7. **Pick a random movie**: Get a random movie suggestion from your collection.
8. **List movies sorted by rating**: Display all movies sorted by their ratings.
9. **List all movies**: Show all movies in the database.
10. **Exit**: Close the application.

## File Structure

- `movies.py`: Main application file with the user interface and core functionality
- `movie_storage.py`: Handles data persistence (loading/saving to JSON)
- `data.json`: JSON file storing the movie database

## Data Format

Movies are stored in a JSON file with the following structure:

```json
{
    "movies": [
        {
            "title": "Movie Title",
            "rating": 8.5,
            "year": 2023
        },
        ...
    ]
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.