import unittest
import json
import os
import tempfile
from unittest.mock import patch
import movie_storage
import movies
import statistics

class TestMovieStats(unittest.TestCase):
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
    
    def test_get_stats_total_movies(self):
        """Test getting the total number of movies."""
        stats = movies.get_stats()
        self.assertEqual(stats["total_movies"], 5)
    
    def test_get_stats_average_rating(self):
        """Test getting the average rating."""
        stats = movies.get_stats()
        # Calculate expected average manually
        ratings = [movie["rating"] for movie in self.sample_movies]
        expected_average = round(statistics.mean(ratings), 2)
        self.assertEqual(stats["average_rating"], expected_average)
    
    def test_get_stats_median_rating(self):
        """Test getting the median rating."""
        stats = movies.get_stats()
        # Calculate expected median manually
        ratings = [movie["rating"] for movie in self.sample_movies]
        expected_median = round(statistics.median(ratings), 2)
        self.assertEqual(stats["median_rating"], expected_median)
    
    def test_get_stats_mode_rating(self):
        """Test getting the mode rating."""
        stats = movies.get_stats()
        # Calculate expected mode manually
        ratings = [movie["rating"] for movie in self.sample_movies]
        expected_mode = statistics.mode(ratings)
        self.assertEqual(stats["mode_rating"], expected_mode)
    
    def test_get_stats_highest_rated(self):
        """Test getting the highest rated movies."""
        stats = movies.get_stats()
        # Find expected highest rated movies manually
        ratings = [movie["rating"] for movie in self.sample_movies]
        max_rating = max(ratings)
        expected_highest = [m for m in self.sample_movies if m["rating"] == max_rating]
        
        # Verify the highest rated movies
        self.assertEqual(len(stats["highest_rated"]), len(expected_highest))
        for movie in expected_highest:
            self.assertIn(movie, stats["highest_rated"])
    
    def test_get_stats_lowest_rated(self):
        """Test getting the lowest rated movies."""
        stats = movies.get_stats()
        # Find expected lowest rated movies manually
        ratings = [movie["rating"] for movie in self.sample_movies]
        min_rating = min(ratings)
        expected_lowest = [m for m in self.sample_movies if m["rating"] == min_rating]
        
        # Verify the lowest rated movies
        self.assertEqual(len(stats["lowest_rated"]), len(expected_lowest))
        for movie in expected_lowest:
            self.assertIn(movie, stats["lowest_rated"])
    
    def test_get_stats_empty_database(self):
        """Test getting stats when there are no movies."""
        # Empty the movies file
        with open(self.temp_filename, 'w') as f:
            json.dump({"movies": []}, f)
        
        # Get stats
        stats = movies.get_stats()
        
        # Verify None is returned
        self.assertIsNone(stats)

if __name__ == '__main__':
    unittest.main()