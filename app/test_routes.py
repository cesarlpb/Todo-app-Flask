# test_routes.py
import sqlite3 as sql
from test_app import app
from flask import render_template, request

# connect to qa_database.sq (database will be created, if not exist)
db_name = 'test.db'
db_table = 'test'
con = sql.connect(db_name)
con.execute(f'CREATE TABLE IF NOT EXISTS {db_table} (ID INTEGER PRIMARY KEY AUTOINCREMENT,'
            + 'Question TEXT, Answer TEXT)')
con.close()

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
    elif request.method == 'POST':
        # read data from the form and save in variable
        question = request.form['question']
        answer = request.form['answer']

        # store in database
        try:
            con = sql.connect(db_name)
            c =  con.cursor() # cursor
            # insert data
            c.execute(f"INSERT INTO {db_table} (question, answer) VALUES (?,?)",
                (question, answer))
            con.commit() # apply changes
            # go to thanks page
            return render_template('test_create_thanks.html', question=question)
        except con.Error as err: # if error
            # then display the error in 'database_error.html' page
            return render_template('test_db_error.html', error=err)
        finally:
            con.close() # close the connection
        
    else:
        return 'Método no permitido', 405 # 400 de Bad Request o 405 de método no permitido

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