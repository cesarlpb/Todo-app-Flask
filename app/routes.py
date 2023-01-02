# routes.py
import sqlite3 as sql # -> quitar import
from app import app
from flask import render_template, request
from utils import *

db_name = 'todo.db'
db_table = 'users'
create_table_if_not_exist(db_name, db_table) # add validation to show error if table not created

# Página de inicio o landing page
@app.route("/")
def index():
    return render_template("home.html")

# Pasos:
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
@app.route("/login")
def login():
    return render_template("login.html")

# Registro de usuario
@app.route("/register")
def register():
    return render_template("register.html")

# Perfil de usuario
@app.route("/profile")
def profile():
    return "Profile"

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