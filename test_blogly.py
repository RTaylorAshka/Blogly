from unittest import TestCase
from app import red_home, get_users, show_user, show_post, new_user_form
from app import app
from flask import session

class FlaskTests(TestCase):
    def test_red_home(self):
       with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 302)
            

    def test_get_users(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text = True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3>Active Users:</h3>', html)

    def test_show_user(self):
        with app.test_client() as client:
            res = client.get('/users/1')
            html = res.get_data(as_text = True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<div class="user-display">', html)

    def test_show_post(self):
        with app.test_client() as client:
            res = client.get('/posts/1')
            html = res.get_data(as_text = True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<a href="/posts/1/edit" class="user-options button">edit</a>', html)

    def test_show_user_form(self):
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text = True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<form action="/users/new" method="post">', html)

    

    

