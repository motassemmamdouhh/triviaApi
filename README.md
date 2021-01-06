

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game,here is the api for the game !
all the backend code follows PEP8 style guidelines
this api will allow you to :
1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started
prerequisits:
python 3.7 and above
Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

and now its all set-up.


## API Reference
the base url is 'localhost/5000' where all the following urls will be added to it

url : '/category', method-allowed : GET, body: None
    this url will return to you all the available categories in the database,status code 200
    and the response body will be like this {
    'success':true,
    category name : example name,
    category id : 1
    }

url : '/questions' , method-allowed: GET, body:None
    This url will return all the questions in the database to be displayed, paginated in 10 questions per page
    the statud code is 200 and response body should be like this {
    'success' : True
    questions: {
      'id': id,
      'question': example question,
      'answer': example answer,
      'category': example category,
      'difficulty': example whole number
      .
      .
      .
      .
      .
      .
      .
    }
    'total_questions' : number of the whole questions in the database
    'total_categories' : number of the whole categories in the database
    }
    
    
url : '/questions/delete', method-allowed:DELETE, parameters: {'question_id': here you put the id of the question to be deleted, which an Int}
    in this url you send the id of a question to be deleted and server reply depends on the proccess,
    on a successful deletion the reply status code is 200 and the body should be like this {
    'success' : True,
    'id_of_deleted_question' : the question id,
    'the_deleted_question' : the question
    }
    if the question does not exist the, the status code is 200 and the reply should be like this {
    'message' : 'no question with this id exists'
    }
    if there is no parameters sent with the request the status code should be 400 and the reply should look like this{
            'success' : False,
            'error': 400,
            'message': "bad request"
        }
    if the server had any trouble deleting the question with an existing id and valid request, the status code should be 500, and the reply looks like this{
            'success' : False,
            'error'  : 500,
            'message' : "internal server error"
            }
    
    
url : '/questions/new', allowed-method : POST,
parameters : {
'question' : the question as a string,
'answer' : answer of the question as a string,
'category' : category of the question as a string,
'difficulty' : difficulty of the question as an Int }
    in this url you send the server a POST request to create a new question using the mentioned parameters for a successful insertion
    if the insertion was successfull the status code should be 200, and the reply looks like this{
            'success' : True,
            'question' : inserted question,
            'answer' : inserted answer,
            'category' : inserted category,
            'difficulty' : inserted difficulty
            }
    if there was a problem in the sent parameters, the status code should be 400, and the reply should be like this{
            'success' : False,
            'error': 400,
            'message': "bad request"
        }
    if the server had any trouble inserting the question with a valid request, the status code should be 500, and the reply looks like this{
            'success' : False,
            'error'  : 500,
            'message' : "internal server error"
            }
            
            
url : '/questions/search', allowed-method: POST, parameters : {search : the term to be searched as a string}
    in this url you send the server a search term and the server replies with the questions which have the search term as a substring in them
    if the search was successful the status code should be 200, and the reply looks like this{
            'success': True,
            'questions' : {
        'id': id,
        'question': example question,
        'answer': example answer,
        'category': example category,
        'difficulty': example whole number
        .
        .
        .
        .
        .
        .
        .
        }
        }
        
url : '/category/<int>/questions', allowed-method: GET, parameters: None
        in this url you send the is of a specific category in the url as mentioned, to get all the questions having the same category.
        if the the category exist the server will reply with the questions paginated in 10 questions per page, the status code should be 200, and the reply looks like this{
            'success' : True,
            'questions' : {
              'id': id,
              'question': example question,
              'answer': example answer,
              'category': example category,
              'difficulty': example whole number
              .
              .
              .
              .
              .
              .
              .
            },
            'current_category' : category.name,
            'total_questions' : len(Question.query.all())
            }
        if the category does not exist, the status code should  be 404 and the reply should look like this{
            'success' : False,
            'error': 404,
            'message': "Not Found"
        }
    
url : '/play', allowed-method : POST, parameters : {past_questions: []}
    in this url you will get a list of random questions having the same category and difficulty, in terms of 10 questions per page
    you should send in the request a list of the already played questions' id so it wont be sent again in the reply
    in case of a successful request the status code should be 200, and the reply should look like this{
            'success' : True,
            'questions' : {
            'id': id,
            'question': example question,
            'answer': example answer,
            'category': example category,
            'difficulty': example whole number
            .
            .
            .
            .
            .
            .
            .
            }
        ,
            'category' : category,
            'difficulty' : difficulty 
            }
    in case of an error in the request, the status code should be 400 and the reply should look like this{
            'success' : False,
            'error': 400,
            'message': "bad request"
        }
        
        
and this is for all the end points of the api.




# Deployment N/a

# Authors
    moatasem abdelkader
    
# Acknowledgements 
the amazing teachers and reviewrs of Udacity