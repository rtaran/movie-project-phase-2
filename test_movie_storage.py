import unittest
import json
import os
import tempfile
from unittest.mock import patch, mock_open
import movie_storage

class TestMovieStorage(unittest.TestCase):
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
    
    def tearDown(self):
        # Remove the temporary file
        self.patcher.stop()
        if os.path.exists(self.temp_filename):
            os.unlink(self.temp_filename)
    
    def test_load_movies_empty_file(self):
        """Test loading movies from an empty file."""
        # Ensure the file exists but is empty
        with open(self.temp_filename, 'w') as f:
            f.write('')
        
        # Should return an empty list when file is empty or invalid
        self.assertEqual(movie_storage.load_movies(), [])
    
    def test_load_movies_valid_file(self):
        """Test loading movies from a valid file."""
        # Create a valid JSON file with sample data
        with open(self.temp_filename, 'w') as f:
            json.dump({"movies": self.sample_movies}, f)
        
        # Should return the list of movies
        self.assertEqual(movie_storage.load_movies(), self.sample_movies)
    
    def test_save_movies(self):
        """Test saving movies to a file."""
        # Save the sample movies
        movie_storage.save_movies(self.sample_movies)
        
        # Read the file and verify content
        with open(self.temp_filename, 'r') as f:
            data = json.load(f)
            self.assertEqual(data["movies"], self.sample_movies)
    
    def test_add_movie(self):
        """Test adding a movie."""
        # Start with an empty file
        with open(self.temp_filename, 'w') as f:
            json.dump({"movies": []}, f)
        
        # Add a movie
        movie_storage.add_movie("New Test Movie", 9.0, 2021)
        
        # Verify the movie was added
        movies = movie_storage.load_movies()
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0]["title"], "New Test Movie")
        self.assertEqual(movies[0]["rating"], 9.0)
        self.assertEqual(movies[0]["year"], 2021)
    
    def test_delete_movie_existing(self):
        """Test deleting an existing movie."""
        # Start with sample movies
        with open(self.temp_filename, 'w') as f:
            json.dump({"movies": self.sample_movies}, f)
        
        # Delete a movie
        result = movie_storage.delete_movie("Test Movie 1")
        
        # Verify the movie was deleted
        self.assertTrue(result)
        movies = movie_storage.load_movies()
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0]["title"], "Test Movie 2")
    
    def test_delete_movie_nonexistent(self):
        """Test deleting a non-existent movie."""
        # Start with sample movies
        with open(self.temp_filename, 'w') as f:
            json.dump({"movies": self.sample_movies}, f)
        
        # Try to delete a non-existent movie
        result = movie_storage.delete_movie("Non-existent Movie")
        
        # Verify no movie was deleted
        self.assertFalse(result)
        movies = movie_storage.load_movies()
        self.assertEqual(len(movies), 2)

if __name__ == '__main__':
    unittest.main()