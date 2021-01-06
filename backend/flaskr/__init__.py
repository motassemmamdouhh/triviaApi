import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import Question, Category, setup_db
import json
QUESTIONS_PER_PAGE = 10
def paginate_questions(request ,selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
 
    #CORS(app, resources={r"*/api*":{origins : '*'}}) 
    # @app.after_request
    # def after_request(response):
    #     response.header.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    #     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

    @app.route('/categories', methods = ['GET'])
    def show_category():

        categories = Category.query.all()
        formatted_categories = [c.format() for c in categories]
        if categories:
            return jsonify({
            'success' : True,
            'categories' : formatted_categories
            })
        else : abort(422)


    @app.route('/questions', methods = ['GET'])
    def show_questions():
        questions = Question.query.all()

        current_questions = paginate_questions(request, questions)
        categories = Category.query.all()
        categories = [c.format() for c in categories]
        return jsonify({
            'success' : True,
            'questions' : current_questions,
            'total_questions' : len(Question.query.all()),
            'total_categories' : categories
        })


    @app.route('/questions/delete', methods = ['DELETE'])
    def delete_question():
        if not request.data:
            abort(400)
        data = request.data.decode()
        data = json.loads(data)
        question_id = data['question_id']
        question = Question.query.get(question_id)
        if not question:
            return jsonify({'message': 'no question with this id exists'})
        name = question.question
        try:
            question.delete()
            return jsonify({
            'success' : True,
            'id_of_deleted_question' : question_id,
            'the_deleted_question' : name
            })
        except:
            abort(500)


    @app.route('/questions/new', methods = ['POST'])
    def create_question():
        if not request.data :
            abort(400) 
        data = request.data.decode()
        data = json.loads(data)
        questionn = data['question']
        answer = data['answer']
        difficulty = data['difficulty']
        category = data['category']
        try:
            question = Question(question = questionn, answer = answer,
            category = category, difficulty = difficulty)
            question.insert()
            print(question.format())
            return jsonify({
            'success' : True,
            'question' : question.question,
            'answer' : question.answer,
            'category' : question.category,
            'difficulty' : question.difficulty
            })
        except: 
            abort(500)




    @app.route('/questions/search', methods=['POST'])
    def search_question():
        if not request.data:
            abort(400)
        data = request.data.decode()
        data = json.loads(data)
        search = data['search']
        print(search)
        questions = Question.query.filter(Question.question.ilike('%{}%'.format(search))).all()
        if not questions:
            return jsonify({'message': 'no question with this id exists'})
        formatted_questions = [c.format() for c in questions]
        return jsonify({
            'success': True,
            'questions' : formatted_questions
        })


    @app.route('/category/<int:category_id>/questions', methods = ['GET'])
    def show_questions_category(category_id):
        category = Category.query.get(category_id)
        questions = Question.query.filter(Question.category == category.name).all()
        if not questions and category:
            abort(400)
        current_questions = paginate_questions(request, questions)
        return jsonify({
            'success' : True,
            'questions' : current_questions,
            'current_category' : category.name,
            'total_questions' : len(Question.query.all())
            })



    @app.route('/play', methods = ['POST'])
    def play():
        data = request.data.decode()
        if not data :
            abort(400)
        data = json.loads(data)
        category = data['category']
        difficulty = data['difficulty']
        #past question is a list of the past questions id to be easir to compare rather than the whole object
        past_questions = data['past_questions']
        questions = Question.query.filter(Question.category == category,Question.difficulty == difficulty).all()
        playing_questions = []
        for q in questions:
            if q.id in past_questions:
                questions.remove(q)
        for i in range(10):
            question = random.choice(questions)
            playing_questions.append(question)
            questions.remove(question)
        return jsonify({
            'success' : True,
            'questions' : playing_questions,
            'category' : category,
            'difficulty' : difficulty 
        })



    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success' : False,
            'error': 404,
            'message': "Not Found"
        }) , 404
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success' : False,
            'error': 422,
            'message': "unprocessable"
        }), 422

    @app.errorhandler(400)
    def baad(error):
        return jsonify({
            'success' : False,
            'error': 400,
            'message': "bad request"
        }), 400

    @app.errorhandler(500)
    def internal_error(error):
            return jsonify({
            'success' : False,
            'error'  : 500,
            'message' : "internal server error"
            }) , 500
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success' : False,
            'error' : 405,
            'message' : "this method is not allowed for this url"
        }), 405

        
    return app