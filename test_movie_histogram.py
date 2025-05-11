import unittest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock
import movie_storage
import movies
from io import StringIO
import sys

class TestMovieHistogram(unittest.TestCase):
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
            {"title": "Interstellar", "rating": 8.6, "year": 2014},
            {"title": "The Godfather", "rating": 9.0, "year": 1972}
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
    
    @patch('matplotlib.pyplot.hist')
    @patch('matplotlib.pyplot.xlabel')
    @patch('matplotlib.pyplot.ylabel')
    @patch('matplotlib.pyplot.title')
    @patch('matplotlib.pyplot.show')
    def test_show_ratings_histogram(self, mock_show, mock_title, mock_ylabel, mock_xlabel, mock_hist):
        """Test showing a histogram of movie ratings."""
        # Call the function
        movies.show_ratings_histogram()
        
        # Verify that matplotlib functions were called
        mock_hist.assert_called_once()
        mock_xlabel.assert_called_once()
        mock_ylabel.assert_called_once()
        mock_title.assert_called_once()
        mock_show.assert_called_once()
        
        # Verify the data passed to hist
        args, kwargs = mock_hist.call_args
        ratings = args[0]
        
        # Verify the ratings match our sample data
        expected_ratings = [movie["rating"] for movie in self.sample_movies]
        self.assertEqual(sorted(ratings), sorted(expected_ratings))
        
        # Verify the bins parameter
        self.assertEqual(kwargs.get('bins', None), 10)
    
    @patch('matplotlib.pyplot.hist')
    @patch('matplotlib.pyplot.xlabel')
    @patch('matplotlib.pyplot.ylabel')
    @patch('matplotlib.pyplot.title')
    @patch('matplotlib.pyplot.show')
    @patch('sys.stdout', new_callable=StringIO)
    def test_show_ratings_histogram_empty(self, mock_stdout, mock_show, mock_title, mock_ylabel, mock_xlabel, mock_hist):
        """Test showing a histogram when there are no movies."""
        # Empty the movies file
        with open(self.temp_filename, 'w') as f:
            json.dump({"movies": []}, f)
        
        # Call the function
        movies.show_ratings_histogram()
        
        # Verify that matplotlib functions were not called
        mock_hist.assert_not_called()
        mock_xlabel.assert_not_called()
        mock_ylabel.assert_not_called()
        mock_title.assert_not_called()
        mock_show.assert_not_called()
        
        # Verify the error message
        output = mock_stdout.getvalue()
        self.assertIn("No movie ratings available", output)
    
    def test_ratings_distribution(self):
        """Test that the ratings distribution is correctly calculated."""
        # Get the ratings from the sample movies
        ratings = [movie["rating"] for movie in self.sample_movies]
        
        # Verify the distribution
        self.assertEqual(ratings.count(8.5), 1)  # Titanic
        self.assertEqual(ratings.count(9.0), 2)  # The Matrix and The Godfather
        self.assertEqual(ratings.count(8.8), 1)  # Inception
        self.assertEqual(ratings.count(8.6), 1)  # Interstellar

if __name__ == '__main__':
    unittest.main()