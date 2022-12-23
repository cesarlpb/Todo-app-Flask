# save this as app.py
from flask import Flask, render_template

app = Flask(__name__)

# Página de inicio o landing page
@app.route("/")
def index():
    return render_template("home.html")

# Inicio de sesión o login
@app.route("/login")
def login():
    return "Login"

# Registro de usuario
@app.route("/register")
def register():
    return "Register"

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

# 5000 - cambiar puerto a uno que esté libre
if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000, debug = True)