import unittest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock
import movie_storage
import movies

class TestMovieOperations(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_filename = self.temp_file.name
        self.temp_file.close()
        
        # Sample movie data for testing
        self.sample_movies = [
            {"title": "Test Movie 1", "rating": 8.5, "year": 2020},
            {"title": "Test Movie 2", "rating": 7.0, "year": 2019}
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
    
    def test_update_movie_rating_existing(self):
        """Test updating the rating of an existing movie."""
        # Update the rating of an existing movie
        result = movies.update_movie_rating("Test Movie 1", 9.5)
        
        # Verify the rating was updated
        self.assertTrue(result)
        updated_movies = movie_storage.load_movies()
        for movie in updated_movies:
            if movie["title"] == "Test Movie 1":
                self.assertEqual(movie["rating"], 9.5)
    
    def test_update_movie_rating_nonexistent(self):
        """Test updating the rating of a non-existent movie."""
        # Try to update the rating of a non-existent movie
        result = movies.update_movie_rating("Non-existent Movie", 9.5)
        
        # Verify the operation failed
        self.assertFalse(result)
        
        # Verify the original movies are unchanged
        updated_movies = movie_storage.load_movies()
        self.assertEqual(len(updated_movies), 2)
        self.assertEqual(updated_movies[0]["title"], "Test Movie 1")
        self.assertEqual(updated_movies[0]["rating"], 8.5)
        self.assertEqual(updated_movies[1]["title"], "Test Movie 2")
        self.assertEqual(updated_movies[1]["rating"], 7.0)
    
    def test_get_movies_sorted_by_rating(self):
        """Test getting movies sorted by rating."""
        # Get movies sorted by rating
        sorted_movies = movies.get_movies_sorted_by_rating()
        
        # Verify the movies are sorted by rating in descending order
        self.assertEqual(len(sorted_movies), 2)
        self.assertEqual(sorted_movies[0]["title"], "Test Movie 1")  # Rating 8.5
        self.assertEqual(sorted_movies[1]["title"], "Test Movie 2")  # Rating 7.0
        
        # Update a rating to verify sorting changes
        movies.update_movie_rating("Test Movie 2", 9.0)
        sorted_movies = movies.get_movies_sorted_by_rating()
        
        # Verify the new sorting
        self.assertEqual(sorted_movies[0]["title"], "Test Movie 2")  # Now rating 9.0
        self.assertEqual(sorted_movies[1]["title"], "Test Movie 1")  # Still rating 8.5
    
    def test_pick_random_movie_internal(self):
        """Test picking a random movie."""
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

if __name__ == '__main__':
    unittest.main()