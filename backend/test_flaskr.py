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
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:password@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def get_questions_by_category_works(self):
        response = self.client().get('/categories/10/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response[0]['questions']) > 0)
        self.assertTrue(response[0]['total_questions'] > 0)

    def create_question_works(self):
        question = {
            'question': 'Is Flask a Python framework?',
            'answer': 'Yes, it is.',
            'category': '1',
            'difficulty': 1
        }
        respone = self.client().post('/questions', json=question)
        data = json.loads(respone.data)
        self.assertEqual(respone.status_code, 200)
        self.assertTrue(data[0]['success'])


    # posting a question with a missing parameter
    def create_question_returns_404(self):
        question = {
            'question': 'Is Flask a Python framework?',
            'category': '1',
            'difficulty': 1
        }
        check = self.client().post('/questions', json=question)
        data = json.loads(check.data)
        self.assertEqual(check.status_code, 400)
        self.assertEqual(data['success'], False)

    def search_question_works(self):
        search_term = {
            'searchTerm': 'Flask',
        }
        response = self.client().get('/questions', json=search_term)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'] > 0)

    def get_categories_work(self):
        # first create a new category and post to the categories endpoint
        category = {
            'type': 'Education'
        }
        response = self.client().post('/categories', json=category)
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['categories']) > 0)


    def get_all_categories_returns_405(self):
        # sending a different method to the categories url
        response = self.client().put('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "Method not allowed for requested url")
        self.assertEqual(data['success'], False)

    def delete_question_works(self):
        # post a question so it can be deleted
        question = {
            'question': 'Is Flask a Python framework?',
            'answer': 'Yes, it is.',
            'category': '1',
            'difficulty': 1
        }
        response = self.client().post('/questions', json=question)
        data = json.loads(response.data)
        question_id = data[0]['question_id']
        # delete the question just created
        response = self.client().delete(f'/questions/{question_id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data[0]['success'])

    def delete_question_returns_404(self):
        # deletes a question that does not exist
        response = self.client().delete(f'/questions/{100}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Requested resource can not be found')
# Make the tests conveniently executable

    def play_quiz_by_category_works(self):
        quiz = {
            'previous_questions': [1, 2, 3],
            'quiz_category': {
                'type': 'Education',
                'id': '1'
            }
        }
        response = self.client().post('/quizzes', json=quiz)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question']['question'])
        # check if the question is not in the previous question
        self.assertTrue(data['question']['id'] not in quiz['previous_questions'])

    def play_quiz_returns_400(self):
        # play quiz with no given parameter
        response = self.client().post('/quizzes')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')


if __name__ == "__main__":
    unittest.main()
