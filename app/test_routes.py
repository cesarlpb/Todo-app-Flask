# routes.py

from test_app import app
from flask import render_template, request

# home page
@app.route('/')  # root : main page
def index():
    # by default, 'render_template' looks inside the folder 'template'
    return render_template('test_index.html')

# Create question
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        # send the form
        return render_template('test_create.html')
    else: # request.method == 'POST':
        # read data from the form and save in variable
        question = request.form['question']
        answer = request.form['answer']

        # store in database
        # add code here

        return render_template('test_create_thanks.html', question=question)


# Display question
@app.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    if request.method == 'GET':
        # send the form
        # add code here to read the question from database
        question = "Not added yet"

        return render_template('test_question.html', question=question)
    else: # request.method == 'POST':
        # read and check answers
        submitted_answer = request.form['answer']

        # add code here to read the answer from database
        correct_answer = "Not added"

        if submitted_answer == correct_answer:
            return render_template('test_correct.html');
        else:
            return render_template('test_sorry.html',
                answer = correct_answer,
                yourAnswer = submitted_answer
            )