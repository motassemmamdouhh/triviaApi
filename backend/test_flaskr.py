import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app() 
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = 'postgresql://postgres:77288399@localhost:5432/trivia'
        setup_db(self.app)
        self.new_question ={
            'question' : 'testing question',
            'answer' : 'testing answer',
            'category' : 'testing category',
            'difficulty' : 'testing difficulty'
        }
        past = [1,2,3,4,5]
        self.play_test = {
            'category' : 'valid category',
            'difficulty' : 'easy',
            'past_questions' : past
        }
        self.search ={
            'search' : 'test'
        }

        # binds the app to the current context
        with self.app.app_context():
          self.db = SQLAlchemy()
          self.db.init_app(self.app)
          self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_categories(self):
        res = self.client().get('/categories')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
    
    def test_category_fail(self):
        res = self.client().get('/categoriess')
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_show_questions(self):
        res = self.client().get('/questions')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['total_categories'])

    def test_show_questions_fail(self):
        res = self.client().post('/questions')
        data = res.get_json()
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_delete_question(self):
        res = self.client().delete('/questions/delete', json={'question_id': 2})
        data = res.get_json()
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue('id_of_deleted_question')
        self.assertTrue('the_deleted_question')

    def test_delete_error(self):
        res = self.client().delete('/questions/delete')
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_create_question(self):
        res = self.client().post('/questions/new', json=self.new_question)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['answer'])
        self.assertTrue(data['category'])
        self.assertTrue(data['difficulty'])
    
    def test_create_question_error(self):
        res = self.client().post('/questions/new')
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
    
    def test_search_question(self):
        res = self.client().post('/questions/search', json=self.search)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
    
    def test_search_questions_error(self):
        res = self.client().post('/questions/search')
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_show_question_category(self):
        res = self.client().get('category/1/questions')
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['total_questions'])

    def test_show_question_category_error(self):
        res = self.client().get('/category/99/questions')
        data = res.get_json()
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_play(self):
        res = self.client().post('/play', json=self.play_test)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['category'])
        self.assertTrue(data['difficulty'])

    def test_play_error(self):
        res = self.client().post('/play')
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])











# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()