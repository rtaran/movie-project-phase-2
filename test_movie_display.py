import unittest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock
import movie_storage
import movies
from io import StringIO
import sys

class TestMovieDisplay(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_filename = self.temp_file.name
        self.temp_file.close()
        
        # Sample movie data for testing
        self.sample_movies = [
            {"title": "Titanic", "rating": 8.5, "year": 1997},
            {"title": "The Matrix", "rating": 9.0, "year": 1999},
            {"title": "Inception", "rating": 8.8, "year": 2010}
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
    
    def test_list_movies_sorted(self):
        """Test listing movies sorted by rating."""
        # Get the sorted movies
        sorted_movies = movies.get_movies_sorted_by_rating()
        
        # Verify the movies are sorted by rating in descending order
        self.assertEqual(len(sorted_movies), 3)
        self.assertEqual(sorted_movies[0]["title"], "The Matrix")  # Rating 9.0
        self.assertEqual(sorted_movies[1]["title"], "Inception")   # Rating 8.8
        self.assertEqual(sorted_movies[2]["title"], "Titanic")     # Rating 8.5
        
        # Verify the ratings are in descending order
        for i in range(len(sorted_movies) - 1):
            self.assertGreaterEqual(sorted_movies[i]["rating"], sorted_movies[i + 1]["rating"])
    
    def test_list_movies(self):
        """Test listing all movies."""
        # Get all movies
        all_movies = movie_storage.load_movies()
        
        # Verify all movies are returned
        self.assertEqual(len(all_movies), 3)
        titles = [movie["title"] for movie in all_movies]
        self.assertIn("Titanic", titles)
        self.assertIn("The Matrix", titles)
        self.assertIn("Inception", titles)
    
    def test_list_movies_empty(self):
        """Test listing movies when there are no movies."""
        # Empty the movies file
        with open(self.temp_filename, 'w') as f:
            json.dump({"movies": []}, f)
        
        # Get all movies
        all_movies = movie_storage.load_movies()
        
        # Verify an empty list is returned
        self.assertEqual(len(all_movies), 0)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_movies_sorted_output(self, mock_stdout):
        """Test the output of list_movies_sorted function."""
        # Call the function that prints to stdout
        movies.list_movies_sorted()
        
        # Get the output
        output = mock_stdout.getvalue()
        
        # Verify the output contains the movie titles in the correct order
        self.assertIn("The Matrix", output)
        self.assertIn("Inception", output)
        self.assertIn("Titanic", output)
        
        # Verify the order of movies in the output
        matrix_pos = output.find("The Matrix")
        inception_pos = output.find("Inception")
        titanic_pos = output.find("Titanic")
        
        self.assertLess(matrix_pos, inception_pos)
        self.assertLess(inception_pos, titanic_pos)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_movies_output(self, mock_stdout):
        """Test the output of list_movies function."""
        # Call the function that prints to stdout
        movies.list_movies()
        
        # Get the output
        output = mock_stdout.getvalue()
        
        # Verify the output contains all movie titles
        self.assertIn("Titanic", output)
        self.assertIn("The Matrix", output)
        self.assertIn("Inception", output)
        
        # Verify the output contains the ratings and years
        self.assertIn("1997", output)
        self.assertIn("1999", output)
        self.assertIn("2010", output)
        self.assertIn("8.5", output)
        self.assertIn("9.0", output)
        self.assertIn("8.8", output)

if __name__ == '__main__':
    unittest.main()