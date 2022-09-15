# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
API DOCUMENTATION

Below are the available endpoints in the base url.

1. Questions
    1. [GET /questions](#get-questions)
    2. [POST /questions](#post-questions)
    3. [DELETE /questions/<question_id>](#delete-questions)
2. Quizzes
    1. [POST /quizzes](#post-quizzes)
3. Categories
    1. [GET /categories](#get-categories)
    2. [GET /categories/<category_id>/questions](#get-categories-questions)

Quizzes
1. POST /quizzes

Each ressource documentation is clearly structured:
1. Description in a few words
2. `curl` example that can directly be used in terminal
3. More descriptive explanation of input & outputs.
4. Example Response.
5. Error Handling (`curl` command to trigger error + error response)

# <a name="get-questions"></a>
### 1. GET /questions

Fetch paginated questions:
```bash
$ curl -X GET http://127.0.0.1:5000/questions?page=1
```
- Fetches a list of dictionaries of questions in which the keys are the ids with all available fields, a list of all categories and number of total questions.
- Request Arguments:
    - **integer** `page` (optional, 10 questions per page, defaults to `1` if not given)
- Request Headers: **None**
- Returns:
    1. List of dict of questions with following fields:
        - **integer** `id`
        - **string** `question`
        - **string** `answer`
        - **string** `category`
        - **integer** `difficulty`
    2. **list** `categories`
    3. **list** `current_category`
    4. **integer** `total_questions`
    5. **boolean** `success`

#### Example response
```js
{
"categories": [
    "music",
    "Art",
    "Stories",
    "Animation",
    "design",
    "Fashion"
  ],
"current_category": [
    "Music",
  ],
"questions": [
    {
      "answer": "David Mark",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "Who is the first man to win a nobel prize in physics?"
    },
    {
      "answer": "Ronaldo",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "Who is the best football player in the world?"
    },

 [...]

  ],
  "success": true,
  "total_questions": 19
}

```
#### Errors
A request with an invalid page will have the below response:

```bash
curl -X GET http://127.0.0.1:5000/questions?page=124
```

will return

```js
{
  "error": 404,
  "message": "Requested resource can not be found",
  "success": false
}

```

# <a name="post-questions"></a>
### 2. POST /questions

Search Questions
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm" : "love"}' -H 'Content-Type: application/json'
```

Create new Question
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "Is there love in sharing?", "category" : "1" , "answer" : "Yes it is!", "difficulty" : 1 }' -H 'Content-Type: application/json'
```

- Searches database for questions with a search term, if provided. Otherwise,
  it will insert a new question into the database.
- Request Arguments: **None**
- Request Headers :
    - if you want to **search** (_application/json_)
        1. **string** `searchTerm` (<span style="color:red">*</span>required)
    - if you want to **insert** (_application/json_)
        1. **string** `question` (<span style="color:red">*</span>required)
        2. **string** `answer` (<span style="color:red">*</span>required)
        3. **string** `category` (<span style="color:red">*</span>required)
        4. **integer** `difficulty` (<span style="color:red">*</span>required)
- Returns:
    - if you searched:
        1. List of dict of `questions` which match the `searchTerm` with following fields:
            - **integer** `id`
            - **string** `question`
            - **string** `answer`
            - **string** `category`
            - **integer** `difficulty`
        2. List of dict of ``current_category`` with following fields:
            - **integer** `id`
            - **string** `type`
        3. **integer** `total_questions`
        4. **boolean** `success`
    - if you inserted:
        1. List of dict of all questions with following fields:
            - **integer** `id`
            - **string** `question`
            - **string** `answer`
            - **string** `category`
            - **integer** `difficulty`
        2. **integer** `total_questions`
        3. **integer** `created`  id from inserted question
        4. **boolean** `success`

#### Example response
Search Questions
```js
{
  "current_category": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },

   [...] // all current categories

  ],
  "questions": [
    {
      "answer": "Jup",
      "category": 1,
      "difficulty": 1,
      "id": 24,
      "question": "Is this a test question?"
    }

  .. with all questions that contains the search term
  
  ],
  "success": true,
  "total_questions": 6
}

```
Create Question
```js
{
  "question_id": 5, // id of question created
  "success": True,
}

```


#### Errors
**Search related**

Searching for a question that does not exist return a 200 status code below:

```bash
curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm" : "this does not exist"}' -H'Content-Type: application/json' 
```

will return

```js
{
"message":'No Result for searched question!'
"success":False
}
```
**Insert related**

If you try to insert a new `question`, but forget to provide a required field, it will throw an `400` error:
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "Is this a question without an answer?", "category" : "1" , "difficulty" : 1 }' -H 'Content-Type: application/json'
```

will return

```js
{
  "error": 400,
  "message": "Answer can not be blank",
  "success": false
}
```
# <a name="delete-questions"></a>
### 3. DELETE /questions/<question_id>

Delete Questions
```bash
curl -X DELETE http://127.0.0.1:5000/questions/10
```
- Deletes specific question based on given id
- Request Arguments:
    - **integer** `question_id`
- Request Headers : **None**
- Returns:
    - **integer** `deleted` Id from deleted question.
    - **boolean** `success`


#### Example response
```js
{
  "deleted": 10,
  "success": true
}
```

### Errors

If you try to delete a `question` which does not exist, it will throw an `400` error:

```bash
curl -X DELETE http://127.0.0.1:5000/questions/7
```
will return
```js
{
  "error": 400,
  "message": "Question with id 7 does not exist.",
  "success": false
}
```

# <a name="post-quizzes"></a>
### 4. POST /quizzes

Play quiz game.
```bash
curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions" : [1, 2, 5], "quiz_category" : {"type" : "Science", "id" : "1"}} ' -H 'Content-Type: application/json'
```
- Plays quiz game by providing a list of already asked questions and a category to ask for a fitting, random question.
- Request Arguments: **None**
- Request Headers :
    1. **list** `previous_questions` with **integer** ids from already asked questions
    1. **dict** `quiz_category` (optional) with keys:
        1.  **string** type
        2. **integer** id from category
- Returns:
    1. Exactly one `question` as **dict** with following fields:
        - **integer** `id`
        - **string** `question`
        - **string** `answer`
        - **string** `category`
        - **integer** `difficulty`
    2. **boolean** `success`

#### Example response
```js
{
  "question": {
    "answer": "Yes",
    "category": 1,
    "difficulty": 1,
    "id": 12,
    "question": "Is udacity a good learning platform?"
  },
  "success": true
}

```
### Errors

If you try to play the quiz game without a a valid JSON body, it will response with an  `400` error.

```bash
curl -X POST http://127.0.0.1:5000/quizzes
```
will return
```js
{
  "error": 400,
  "message": "Please provide a JSON body with previous question Ids and optional category.",
  "success": false
}

```
# <a name="get-categories"></a>
### 5. GET /categories

Fetch all available categories

```bash
curl -X GET http://127.0.0.1:5000/categories
```

- Fetches a list of all `categories` with its `type` as values.
- Request Arguments: **None**
- Request Headers : **None**
- Returns: A list of categories with its `type` as values
  and a `success` value which indicates status of response.

#### Example response
```js
{
  "categories": [
    "music",
    "Art",
    "Stories",
    "Animation",
    "design",
    "Fashion"
  ],
  "success": True
}
```

# <a name="get-categories-questions"></a>
### 6. GET /categories/<category_id>/questions

Get all questions from a specific `category`.
```bash
curl -X GET http://127.0.0.1:5000/categories/2/questions?page=1
```
- Fetches all `questions` (paginated) from one specific category.
- Request Arguments:
    - **integer** `category_id` (<span style="color:red">*</span>required)
    - **integer** `page` (optinal, 10 questions per Page, defaults to `1` if not given)
- Request Headers: **None**
- Returns:
    1. **integer** `current_category` id from inputted category
    2. List of dict of all questions with following fields:
        - **integer** `id`
        - **string** `question`
        - **string** `answer`
        - **string** `category`
        - **integer** `difficulty`
    3. **integer** `total_questions`
    4. **boolean** `success`

#### Example response

```js
{
  "current_category": "2",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

### Errors
You get a 404 error when you query with a category that doesn't exist or for the wrong page:
```bash
curl -X GET http://127.0.0.1:5000/categories/10/questions?page=1
```
will return
```js
{
  "success": False,
  "error": 404,
  "message": "Requested resource can not be found"
            
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
