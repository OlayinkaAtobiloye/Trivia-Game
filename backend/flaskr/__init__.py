import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    def paginator(request, requested_data):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        formatted_data = [data.format() for data in requested_data]
        current_data = formatted_data[start:end]
        return current_data

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        categories = [category.format() for category in categories]
        categories = [data['type'] for data in categories]
        return jsonify({'success': True,
                        'categories': categories})

    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        questions_paginated = paginator(request, questions)
        if len(questions_paginated) == 0:
            abort(404)
        categories = [category.format() for category in Category.query.all()]
        categories_list = [data['type'] for data in categories]
        current_category = categories_list
        return jsonify({'questions': questions_paginated, 'total_questions': len(questions),
                        'current_category': current_category, 'categories': categories_list})

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter_by(id=question_id).one_or_none()
        if question is None:
            abort(404)
        try:
            question.delete()
            return jsonify({'success': True, 'question_id': question.id}, 200)
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def post_or_search_question():
        request_body = request.get_json()
        if not request_body:
            abort(400)
        search_term = request.get_json().get('searchTerm', None)
        if search_term:
            questions = Question.query.filter(Question.question.ilike(f'% {search_term} %')).all()
            if questions:
                formatted_questions = [question.format() for question in questions]
                return jsonify({'question': formatted_questions,
                                'total_question': len(formatted_questions),
                                'current_category': questions[0].category,
                                'success': True})
            else:
                abort(404)
        question = request_body.get('question')
        answer = request_body.get('answer')
        difficulty = request_body.get('difficulty')
        category = request_body.get('category')
        if not question or not answer or not difficulty or not category:
            abort(400)
        try:
            new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
            new_question.insert()
            return jsonify({'success': True, 'question_id': new_question.id}, 201)
        except Exception as e:
            abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def get_question_by_category(category_id):
        category = Category.query.get(category_id)
        if category is None:
            abort(404)
        questions = (Question.query.filter(Question.category == str(category_id)).order_by(Question.id).all())
        formatted_questions = paginator(request, questions)
        return jsonify({'success': True, 'questions': formatted_questions, 'total_questions': len(questions),
                        'current_category': category_id}, 200)

    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        request_body = request.get_json()
        if request_body is None:
            abort(404)
        previous_questions = request_body.get('previous_questions', None)
        quiz_category = request_body.get('quiz_category', None)
        if not previous_questions:
            if quiz_category:
                question_list = Question.query.filter(Question.category == (quiz_category['id'])).all()
            else:
                question_list = Question.query.all()
        else:
            if quiz_category:
                question_list = Question.query.filter(Question.category == str(quiz_category['id'])). \
                    filter(Question.id.notin_(previous_questions)).all()
            else:
                question_list = Question.query.filter(Question.id.notin_(previous_questions)).all()
        formatted_questions = [question.format() for question in question_list]
        total = len(formatted_questions)
        if total == 1:
            random_question = formatted_questions[0]
        else:
            random_question = formatted_questions[random.randint(0, len(formatted_questions))]

        return jsonify({
            'success': True,
            'question': random_question
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Requested resource can not be found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed for requested url"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": 'Request can not be processed'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app


app = create_app()
