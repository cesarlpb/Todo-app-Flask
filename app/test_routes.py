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
        
        # return render_template('test_create_thanks.html', question=question)

    else:
        return 'Método no permitido', 405 # 400 de Bad Request o 405 de método no permitido

# Display all questions in db
@app.route('/questions', methods=['GET'])
def questions():
    # read from database
    try:
        con = sql.connect(db_name)
        c =  con.cursor() # cursor
        # read data
        c.execute(f"SELECT ID, Question FROM {db_table}")
        questions = c.fetchall()   # tomamos todos los valores del select
        con.commit() # apply changes
        return render_template('test_questions.html', questions=questions)
    except con.Error as err: # if error
        # then display the error in 'database_error.html' page
        return render_template('test_db_error.html', error=err)
    finally:
        con.close() # close the connection
    
    # return render_template('test_questions.html', questions=questions)  # revisar

# Display question
@app.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    if request.method == 'GET':
        # send the form
        # code to read the question from database
        try:
            con = sql.connect(db_name)
            c =  con.cursor() # cursor
            # read question : SQLite index start from 1 (see index.html)
            query = f"Select Question FROM {db_table} where id = {id}"
            c.execute(query)
            question = c.fetchone() # fetch the data from cursor
            con.commit() # apply changes
            # go to thanks page : pass the value of tuple using question[0]
            return render_template('test_question.html', question=question[0])
        except con.Error as err: # if error
            # then display the error in 'database_error.html' page
            return render_template('test_db_error.html', error=err)
        finally:
            con.close() # close the connection

        return render_template('test_question.html', question=question) # revisar
    else: # request.method == 'POST':
        # read and check answers
        submitted_answer = request.form['answer']

        # code to read the answer from database
        try:
            con = sql.connect(db_name)
            c =  con.cursor() # cursor
            # read answer : SQLite index start from 1 (see index.html)
            
            query = f"Select Answer FROM {db_table} where id = {id}" # revisar
            # query = f"Select Answer FROM {db_table} where id = {0}".format(id)

            c.execute(query)
            correct_answer = c.fetchone()[0] # fetch and store tuple-value (see [0])
            con.commit() # apply changes
        except con.Error as err: # if error
            # then display the error in 'database_error.html' page
            return render_template('test_db_error.html', error=err)
        finally:
            con.close() # close the connection

        if submitted_answer == correct_answer:
            return render_template('test_correct.html');
        else:
            return render_template('test_sorry.html',
                answer = correct_answer,
                yourAnswer = submitted_answer
            )

# Edit question
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    
    # if request.form['question'] != None or request.form['question'] != "":
    # update test set question = question, answer = answer where id = id
    # html -> id
    if request.method == 'GET':
        try:
            con = sql.connect(db_name)
            c =  con.cursor()
            c.execute(f"SELECT * FROM {db_table} WHERE id = {id}")
            id, question, answer = c.fetchone() # current values for id, question, answer
            con.commit()
            return render_template('test_edit.html', id=id, question=question, answer=answer)
        except con.Error as err: # if error
            # then display the error in 'database_error.html' page
            return render_template('test_db_error.html', error=err)
        finally:
            con.close()
    elif request.method == 'POST':
        # id MUST NOT be changed
            # We store values from form
        new_question = request.form['question']
        new_answer = request.form['answer']
        
        # We read current values from database
        try:
            con = sql.connect(db_name)
            c =  con.cursor()
            c.execute(f"SELECT Question, Answer FROM {db_table} WHERE id = {id}")
            question, answer = c.fetchone() # current values for id, question, answer
            con.commit()
        except con.Error as err: # if error
            # then display the error in 'database_error.html' page
            return render_template('test_db_error.html', error=err)
        finally:
            con.close()
        
        # We validate NOT to have empty fields for update
        if new_question != None or new_question != "":
            question = new_question
        if new_answer != None or new_answer != "":
            answer = new_answer
        
        # Finally, we update the database
        try:
            con = sql.connect(db_name)
            c =  con.cursor() # cursor
            
            print(f"UPDATE {db_table} SET Question={question}, Answer={answer} WHERE id = {id}")
            c.execute(f"UPDATE {db_table} SET Question={question}, Answer={answer} WHERE id = {id}")
            con.commit() # apply changes

            # Reading data to display in thanks page
            c.execute(f"SELECT Question, Answer FROM {db_table} WHERE id = {id}")
            question, answer = c.fetchone() # current values for id, question, answer
            print(question, answer)
            con.commit()
            # go to thanks page
            return render_template('test_edit_thanks.html', id=id, question=question, answer=answer)
        except con.Error as err: # if error
            # then display the error in 'database_error.html' page
            return render_template('test_db_error.html', error=err)
        finally:
            con.close() # close the connection
# Delete question
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    # html thanks page -> id
        # "Se ha borrado la pregunta con id: id" 
    try:
        con = sql.connect(db_name)
        c =  con.cursor() # cursor
        c.execute(f"DELETE FROM {db_table} WHERE id = {id}")
        con.commit() # apply changes
        return render_template('test_delete_thanks.html', id = id)
    except con.Error as err: # if error
        # then display the error in 'database_error.html' page
        return render_template('test_db_error.html', error=err)
    finally:
        con.close() # close the connection