# routes.py
from app import app
from flask import render_template, request, session, redirect, url_for
from utils import *

app.secret_key = 'your secret key' 

db_name = 'todo.db'
db_table = 'users'
todos_table = 'todos'
create_tables_if_not_exist(db_name, db_table, todos_table) # add validation to show error if table not created
# Página de inicio o landing page
@app.route("/")
def index():
    return render_template("home.html", logged_in = bool(session['logged_in']) if 'logged_in' in session else False)

# Inicio de sesión o login
@app.route("/login", methods =['GET', 'POST'])
def login():
    # msg = ""
    if request.method == 'GET':
        return render_template("login.html", logged_in = bool(session['logged_in']) if 'logged_in' in session else False)
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account = login_user(db_name, db_table, username, password) # (1, 'test@test.test', '12345', 'test1') o None
        if account:
            session['logged_in'] = True
            session['id'] = account[0] # id
            session['username'] = account[-1] # username
            return redirect(url_for('profile', username = session['username'])) # Todo: añadir opciones para editar perfil de usuario (Ejercicio)
        else:
            error = 'Hay algún dato incorrecto. Vuelve a intentarlo.'
    return render_template("login.html", error=error, logged_in = bool(session['logged_in']) if 'logged_in' in session else False)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('username', None)
    session['logout_msg'] = "Has salido de sesión."
    return render_template('login.html', logout_msg=session['logout_msg'], logged_in = bool(session['logged_in']) if 'logged_in' in session else False) # redirect to login page

# Registro de usuario
@app.route("/register", methods =['GET', 'POST'])
def register():
    msg = ""
    if request.method == 'GET':
        return render_template("register.html", logged_in = bool(session['logged_in']) if 'logged_in' in session else False)
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        # read data from the form and save in variable
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # password2 = request.form['password2']

        # store in database
        can_register_user, msg, es_warning = register_user(db_name, db_table, username, email, password)
        # revisar
        if isinstance(can_register_user, bool) and can_register_user:
            return render_template('register_thanks.html', username=username, msg=msg, es_warning=es_warning, logged_in = bool(session['logged_in']) if 'logged_in' in session else False) # es_warning = False
        elif isinstance(can_register_user, bool) and not can_register_user:
            return render_template('register.html', error=f"{msg}\nUsuario no registrado. Vuelve a intentarlo", es_warning=es_warning, logged_in = bool(session['logged_in']) if 'logged_in' in session else False) # es_warning = True
        else:
            con_error = can_register_user
            return render_template('register.html', error=f"{con_error}\nUsuario no registrado. Vuelve a intentarlo", es_warning=False, logged_in = bool(session['logged_in']) if 'logged_in' in session else False)
    elif request.method == 'POST':
        msg = "Por favor, rellena todos los campos"
    return render_template('register.html', msg=msg, logged_in = bool(session['logged_in']) if 'logged_in' in session else False)
# Perfil de usuario
@app.route("/profile")
def profile():
    # Ejericio: añadir opciones para editar perfil de usuario
    return render_template('profile.html', username = session['username'], msg='Has iniciado sesión correctamente !', logged_in = bool(session['logged_in']) if 'logged_in' in session else False)

# Gestión de notas -> CRUD
    # Create -> Crear nota
    # Read -> Leer nota -> una o todas
    # Update -> Actualizar nota
    # Delete -> Eliminar nota

# Debe estar logeado -> ruta para ver TODAS las notas del usuario
@app.route("/todos")
def get_all_todos():
    todos = read_all_todos(db_name, todos_table, session['id'])
    return render_template('todos.html', todos=todos, logged_in = bool(session['logged_in']) if 'logged_in' in session else False)

# Debe estar logeado -> ruta para ver UNA nota del usuario
@app.route("/todos/<int:id>")
def get_todo(id):
    todo = read_todo_by_id(db_name, todos_table,  session['id'], id)
    return render_template('todo.html', todo=todo, logged_in = bool(session['logged_in']) if 'logged_in' in session else False)

# Debe estar logeado -> ruta para crear una nota
@app.route("/create", methods=["GET", "POST"])
def create_todo():
    if request.method == 'GET':
        return render_template('create_todo.html', logged_in = bool(session['logged_in']) if 'logged_in' in session else False)
    elif request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        done = 0 # 0 = Pendiente, 1 = Hecho/Completado
        can_create_todo, msg = create_new_todo(db_name, todos_table, session['id'], [title, description, done]) 
        # Validar si se ha creado la nota con can_create_todo
        return render_template('create_thanks.html', msg=msg, logged_in = bool(session['logged_in']) if 'logged_in' in session else False)

# Debe estar logeado -> ruta para actualizar una nota
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_todo(id):
    if request.method == 'GET':
        todo = read_todo_by_id(db_name, todos_table,  session['id'], id)
        return render_template('update_todo.html', todo=todo, logged_in = bool(session['logged_in']) if 'logged_in' in session else False)
    elif request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        if 'done' in request.form and request.form['done']:
            done = int(request.form['done']) # 0 = Pendiente, 1 = Hecho/Completado
        else:
            done = 0
        can_update_todo, msg = update_todo_by_id(db_name, todos_table, session['id'], id, [title, description, done])
        # Validar si se ha actualizado la nota con can_update_todo
        if can_update_todo:
            return render_template('update_thanks.html', msg=msg, logged_in = bool(session['logged_in']) if 'logged_in' in session else False)
        else:
            return f"error: {can_update_todo}"

# Debe estar logeado -> ruta para eliminar una nota
@app.route("/delete/<int:id>", methods=["GET"])
def delete_todo(id):
    if request.method == 'GET':
        can_delete_todo, msg = delete_todo_by_id(db_name, todos_table, session['id'], id)
        # Validar si se ha eliminado la nota con can_delete_todo
        if can_delete_todo:
            return render_template('delete_thanks.html', id=id, msg=msg, logged_in = bool(session['logged_in']) if 'logged_in' in session else False)

# Página de error
@app.errorhandler(404)
def page_not_found(e):
    # return "Esta ruta no existe", 404
    return render_template("404.html", msg="Esta página no existe :(", logged_in = bool(session['logged_in']) if 'logged_in' in session else False), 404