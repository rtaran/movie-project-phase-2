import unittest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock
import movie_storage
import movies
from io import StringIO
import sys
import random

class TestMovieRandom(unittest.TestCase):
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
    
    def test_pick_random_movie_internal(self):
        """Test picking a random movie internally."""
        # Set a fixed seed for reproducibility
        random.seed(42)
        
        # Pick a random movie
        random_movie = movies.pick_random_movie_internal()
        
        # Verify the movie is one of the sample movies
        self.assertIn(random_movie, self.sample_movies)
    
    def test_pick_random_movie_internal_empty(self):
        """Test picking a random movie when there are no movies."""
        # Empty the movies file
        with open(self.temp_filename, 'w') as f:
            json.dump({"movies": []}, f)
        
        # Try to pick a random movie
        random_movie = movies.pick_random_movie_internal()
        
        # Verify None is returned
        self.assertIsNone(random_movie)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_pick_random_movie_output(self, mock_stdout):
        """Test the output of pick_random_movie function."""
        # Mock the pick_random_movie_internal function to return a fixed movie
        fixed_movie = self.sample_movies[0]
        with patch('movies.pick_random_movie_internal', return_value=fixed_movie):
            # Call the function that prints to stdout
            movies.pick_random_movie()
            
            # Get the output
            output = mock_stdout.getvalue()
            
            # Verify the output contains the movie title, year, and rating
            self.assertIn(fixed_movie["title"], output)
            self.assertIn(str(fixed_movie["year"]), output)
            self.assertIn(str(fixed_movie["rating"]), output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_pick_random_movie_output_empty(self, mock_stdout):
        """Test the output of pick_random_movie function when there are no movies."""
        # Mock the pick_random_movie_internal function to return None
        with patch('movies.pick_random_movie_internal', return_value=None):
            # Call the function that prints to stdout
            movies.pick_random_movie()
            
            # Get the output
            output = mock_stdout.getvalue()
            
            # Verify the output indicates no movies are available
            self.assertIn("No movies available", output)
    
    def test_random_distribution(self):
        """Test that the random selection is reasonably distributed."""
        # This test is more of a statistical test and might occasionally fail
        # due to the nature of randomness, but it should pass most of the time.
        
        # Add more movies to get a better distribution
        movies_list = movie_storage.load_movies()
        for i in range(7):
            movies_list.append({"title": f"Test Movie {i}", "rating": 7.0, "year": 2000})
        movie_storage.save_movies(movies_list)
        
        # Count occurrences of each movie
        counts = {movie["title"]: 0 for movie in movies_list}
        
        # Pick random movies many times
        num_picks = 1000
        for _ in range(num_picks):
            random_movie = movies.pick_random_movie_internal()
            counts[random_movie["title"]] += 1
        
        # Verify each movie was picked at least once
        for title, count in counts.items():
            self.assertGreater(count, 0, f"Movie '{title}' was never picked")
        
        # Verify no movie was picked too frequently (more than 30% of the time)
        for title, count in counts.items():
            self.assertLess(count / num_picks, 0.3, f"Movie '{title}' was picked too frequently")

if __name__ == '__main__':
    unittest.main()