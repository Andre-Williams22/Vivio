# tests.py

from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId
from datetime import datetime


sample_movie_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_movie = {
    'title': 'Cat Videos',
    'description': 'Cats acting weird',
    'videos': [
        'https://youtube.com/embed/hY7m5jjJ9mM'
    ]
}





class MoviesTests(TestCase):
    """Flask tests."""
 
    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        
    def test_index(self):
        """Test the movies homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Movies', result.data)
        
        
    def test_new(self):
        """Test the new movie creation page."""
        result = self.client.get('/movies/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Movie', result.data)

    # @mock.patch("stripe.Customer.create")
    # def test_charge(self, mock_customer_create):
    #     """Test the charge page."""
    #     mock_customer_create.return_value='sample@customer.com', '6ff543682')
    #     result = self.client.post('/charge', data={'stripeToken':'6ff543682'})
    #     self.assertEqual(result.status, '302 FOUND')
    #     self.assertIn(b'charge', result.data)
    #     mock_customer_create.assert_called_with('sample@customer.com', '6ff543682')
        
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_movie(self, mock_find):
        """Test showing a single movie."""
        mock_find.return_value = sample_movie

        result = self.client.get(f'/movies/{sample_movie_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cats acting weird', result.data)
        
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_movie(self, mock_find):
        """Test editing a single movie."""
        mock_find.return_value = sample_movie

        result = self.client.get(f'/movies/{sample_movie_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cats acting weird', result.data)
        
    # @mock.patch('pymongo.collection.Collection.insert_one')
    # @mock.patch('datetime.now')
    # def test_submit_movie(self, mock_insert):
    #     """Test submitting a new movie."""
    #     result = self.client.post('/movies', data=sample_movie)

    #     # After submitting, should redirect to that movie's page
    #     self.assertEqual(result.status, '302 FOUND')
    #     mock_insert.assert_called_with(sample_movie)
    
    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_movie(self, mock_update):
        form_data = {'_method': 'PUT', **sample_movie}
        result = self.client.post(f'/movies/{sample_movie_id}', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_movie_id}, {'$set': sample_movie})
        
    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_movie(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/movies/{sample_movie_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_movie_id})


if __name__ == '__main__':
    unittest_main()