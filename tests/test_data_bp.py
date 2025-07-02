
import unittest
from unittest.mock import patch, MagicMock
import json
import jwt
from minicrud.app import create_app
from minicrud.database import db
from minicrud.models import User, Data

class DataBPTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.init_app(cls.app)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # Create a test user
        self.user = User(username='testuser', email='test@example.com', api_token='testtoken')
        db.session.add(self.user)
        db.session.commit()

        # Mock jwt.decode and User.query.filter_by().first()
        self.patcher_jwt_decode = patch('minicrud.auth.jwt.decode')
        self.mock_jwt_decode = self.patcher_jwt_decode.start()
        self.mock_jwt_decode.return_value = {'id': self.user.id}

        self.patcher_user_query = patch('minicrud.auth.User.query')
        self.mock_user_query = self.patcher_user_query.start()
        self.mock_user_query.filter_by.return_value.first.return_value = self.user

    def tearDown(self):
        self.patcher_jwt_decode.stop()
        self.patcher_user_query.stop()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('minicrud.blueprints.data_bp.db.session.add')
    @patch('minicrud.blueprints.data_bp.db.session.commit')
    def test_create_data(self, mock_commit, mock_add):
        with self.app.app_context():
            response = self.client.post('/data',
                                        data=json.dumps({'text': 'Test data'}),
                                        content_type='application/json',
                                        headers={'x-access-token': 'testtoken'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'New data created!', response.data)

    @patch('minicrud.blueprints.data_bp.Data.query')
    def test_get_all_data(self, mock_query):
        with self.app.app_context():
            # Mock the database query
            mock_data = [Data(id=1, text='Test data 1', user_id=self.user.id),
                         Data(id=2, text='Test data 2', user_id=self.user.id)]
            mock_query.filter_by.return_value.all.return_value = mock_data

            response = self.client.get('/data', headers={'x-access-token': 'testtoken'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test data 1', response.data)
            self.assertIn(b'Test data 2', response.data)

    @patch('minicrud.blueprints.data_bp.Data.query')
    def test_get_one_data(self, mock_query):
        with self.app.app_context():
            # Mock the database query
            mock_data = Data(id=1, text='Test data 1', user_id=self.user.id)
            mock_query.filter_by.return_value.first.return_value = mock_data

            response = self.client.get('/data/1', headers={'x-access-token': 'testtoken'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test data 1', response.data)

    @patch('minicrud.blueprints.data_bp.Data.query')
    @patch('minicrud.blueprints.data_bp.db.session.commit')
    def test_update_data(self, mock_commit, mock_query):
        with self.app.app_context():
            # Mock the database query
            mock_data = Data(id=1, text='Test data 1', user_id=self.user.id)
            mock_query.filter_by.return_value.first.return_value = mock_data

            response = self.client.put('/data/1',
                                       data=json.dumps({'text': 'Updated data'}),
                                       content_type='application/json',
                                       headers={'x-access-token': 'testtoken'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Data has been updated!', response.data)

    @patch('minicrud.blueprints.data_bp.Data.query')
    @patch('minicrud.blueprints.data_bp.db.session.delete')
    @patch('minicrud.blueprints.data_bp.db.session.commit')
    def test_delete_data(self, mock_commit, mock_delete, mock_query):
        with self.app.app_context():
            # Mock the database query
            mock_data = Data(id=1, text='Test data 1', user_id=self.user.id)
            mock_query.filter_by.return_value.first.return_value = mock_data

            response = self.client.delete('/data/1', headers={'x-access-token': 'testtoken'})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Data has been deleted!', response.data)

if __name__ == '__main__':
    unittest.main()
