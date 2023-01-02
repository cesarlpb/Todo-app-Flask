# routes.py
import sqlite3 as sql # -> quitar import
from app import app
from flask import render_template, request, session, redirect, url_for
from utils import *

app.secret_key = 'your secret key' 

db_name = 'todo.db'
db_table = 'users'
create_table_if_not_exist(db_name, db_table) # add validation to show error if table not created

# Página de inicio o landing page
@app.route("/")
def index():
    return render_template("home.html")

# Pasos:

# X Crear tabla users

## Registro:
    # X Crear formulario de registro
        # condiciones sobre la contraseña
            # pedir repetir contraseña y comprobar si son iguales
        # condiciones sobre el usuario
        # validar email ?
    # X Ruta -> /register
    # 3. Validar datos -> en la base de datos -> no repetir usuario
    # 4. Si es correcto -> redirigir a /profile o a /login o a /
## Login:
    # X Crear formulario de login
    # X Ruta -> /login
    # 3. Validar datos -> en la base de datos
        # usar session para guardar el usuario logeado
    # 4. Si es correcto -> redirigir a /profile

## Una vez el usuario logea -> puede acceder a las rutas de los todos
    # Si no ha logeado solo puede ver /, /login, /register

# Conexiones a bd de SQLite3 con utils.py

# Inicio de sesión o login
@app.route("/login", methods =['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account = login_user(db_name, db_table, username, password) # (1, 'test@test.test', '12345', 'test1') o None
        if account:
            session['logged_in'] = True
            session['id'] = account[0] # id
            session['username'] = account[-1] # username
            return redirect(url_for('profile', username = session['username']))
            # return render_template('profile.html', msg = msg, username = session['username'])
        else:
            error = 'Hay algún dato incorrecto. Vuelve a intentarlo.'
    return render_template("login.html", error=error)

# Registro de usuario
@app.route("/register", methods =['GET', 'POST'])
def register():
    msg = ""
    if request.method == 'GET':
        return render_template("register.html")
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
            return render_template('register_thanks.html', username=username, msg=msg, es_warning=es_warning) # es_warning = False
        elif isinstance(can_register_user, bool) and not can_register_user:
            return render_template('register.html', error=f"{msg}\nUsuario no registrado. Vuelve a intentarlo", es_warning=es_warning) # es_warning = True
        else:
            con_error = can_register_user
            return render_template('register.html', error=f"{con_error}\nUsuario no registrado. Vuelve a intentarlo", es_warning=False)
    elif request.method == 'POST':
        msg = "Por favor, rellena todos los campos"
    return render_template('register.html', msg=msg)
# Perfil de usuario
@app.route("/profile")
def profile():
    return render_template('profile.html', username = session['username'], msg='Has iniciado sesión correctamente !')

# Gestión de notas -> CRUD
    # Create -> Crear nota
    # Read -> Leer nota -> una o todas
    # Update -> Actualizar nota
    # Delete -> Eliminar nota

# Debe estar logeado -> ruta para ver TODAS las notas del usuario
@app.route("/todos")
def get_all_todos():
    return "All Todos"

# Debe estar logeado -> ruta para ver UNA nota del usuario
@app.route("/todos/<int:id>")
def get_todo(id):
    return f"Todo {id}"

# Debe estar logeado -> ruta para crear una nota
@app.route("/create", methods=["GET", "POST"])
def create_todo():
    return "Create"

# Debe estar logeado -> ruta para actualizar una nota
@app.route("/update/<int:id>", methods=["GET", "PUT"])
def update_todo(id):
    return f"Update {id}"

# Debe estar logeado -> ruta para eliminar una nota
@app.route("/delete/<int:id>", methods=["GET", "DELETE"])
def delete_todo(id):
    return f"Delete {id}"

# Página de error
@app.errorhandler(404)
def page_not_found(e):
    return "Esta ruta no existe", 404
    # return render_template("404.html"), 404