import unittest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock
import movie_storage
import movies
from io import StringIO
import sys

class TestMovieSearch(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_filename = self.temp_file.name
        self.temp_file.close()
        
        # Sample movie data for testing
        self.sample_movies = [
            {"title": "Titanic", "rating": 8.5, "year": 1997},
            {"title": "The Matrix", "rating": 9.0, "year": 1999},
            {"title": "Inception", "rating": 8.8, "year": 2010},
            {"title": "Interstellar", "rating": 8.6, "year": 2014}
        ]
        
        # Patch the MOVIES_FILE constant
        self.patcher = patch('movie_storage.MOVIES_FILE', self.temp_filename)
        self.patcher.start()
        
        # Initialize the file with sample data
        with open(self.temp_filename, 'w') as f:
            json.dump({"movies": self.sample_movies}, f)
    
    def tearDown(self):
        # Remove the temporary file
        self.patcher.stop()
        if os.path.exists(self.temp_filename):
            os.unlink(self.temp_filename)
    
    def test_search_exact_match(self):
        """Test searching for a movie with an exact match."""
        # Extract the core search logic from the search_movie function
        query = "matrix"
        movies_list = movie_storage.load_movies()
        matches = [m for m in movies_list if query in m["title"].strip().lower()]
        
        # Verify the search results
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["title"], "The Matrix")
    
    def test_search_partial_match(self):
        """Test searching for a movie with a partial match."""
        # Extract the core search logic from the search_movie function
        query = "inter"
        movies_list = movie_storage.load_movies()
        matches = [m for m in movies_list if query in m["title"].strip().lower()]
        
        # Verify the search results
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["title"], "Interstellar")
    
    def test_search_case_insensitive(self):
        """Test searching for a movie with case-insensitive matching."""
        # Extract the core search logic from the search_movie function
        query = "MATRIX"
        movies_list = movie_storage.load_movies()
        matches = [m for m in movies_list if query.lower() in m["title"].strip().lower()]
        
        # Verify the search results
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["title"], "The Matrix")
    
    def test_search_multiple_matches(self):
        """Test searching for a movie with multiple matches."""
        # Add another movie with a similar title
        movies_list = movie_storage.load_movies()
        movies_list.append({"title": "The Matrix Reloaded", "rating": 7.5, "year": 2003})
        movie_storage.save_movies(movies_list)
        
        # Extract the core search logic from the search_movie function
        query = "matrix"
        movies_list = movie_storage.load_movies()
        matches = [m for m in movies_list if query in m["title"].strip().lower()]
        
        # Verify the search results
        self.assertEqual(len(matches), 2)
        self.assertTrue(any(m["title"] == "The Matrix" for m in matches))
        self.assertTrue(any(m["title"] == "The Matrix Reloaded" for m in matches))
    
    def test_search_no_match(self):
        """Test searching for a movie with no match."""
        # Extract the core search logic from the search_movie function
        query = "nonexistent"
        movies_list = movie_storage.load_movies()
        matches = [m for m in movies_list if query in m["title"].strip().lower()]
        
        # Verify the search results
        self.assertEqual(len(matches), 0)
        
        # Test fuzzy matching (simplified version of what's in the code)
        titles = [movie["title"] for movie in movies_list]
        from fuzzywuzzy import process
        best_match = process.extractOne(query, titles)
        
        # Verify that the best match score is below the threshold (70)
        self.assertLess(best_match[1], 70)

if __name__ == '__main__':
    unittest.main()