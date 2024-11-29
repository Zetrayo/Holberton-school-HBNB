import unittest
from app import create_app, db  # Adjust according to your app structure
from app.models.user import User  # Ensure this imports the User class

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        """Create a test client and set up the application."""
        self.app = create_app('testing')  # Use your testing configuration
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()  # Create test database tables

        # Create a test user for login tests
        self.test_user = User(
            first_name="Testing", 
            last_name="Testing", 
            email='test@example.com', 
            password=User.hash_password('testpassword')
)
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        """Clean up the database after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register(self):
        """Test user registration."""
        response = self.client.post('api/v1/users/register', json={
            'first_name': 'TestingUser',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('User successfully created', str(response.data))

    def test_login(self):
        """Test user login."""
        response = self.client.post('api/v1/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpassword'
        })

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('access_token', data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post('api/v1/auth/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })

        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', str(response.data))

if __name__ == '__main__':  
    unittest.main()