#%% utils.py
import sqlite3 as sql
import re
from datetime import datetime, timedelta

# Create table if not exist
def create_tables_if_not_exist(db_name : str, users_table : str, todos_table : str) -> bool | sql.Error:
    """
        Crea las tablas si no existen -> users y todos

        Args: db_name (str): bd, users_table (str): tabla users, todos_table (str): tabla todos,

        Returns: bool | sql.Error: True si se crearon las tablas, False si no se crearon las tablas y sql.Error si hubo un error
    """
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        # Start a transaction
        c.execute('BEGIN')
        # Tabla users
        c.execute(f"CREATE TABLE IF NOT EXISTS {users_table} (Id INTEGER PRIMARY KEY AUTOINCREMENT, Email TEXT, Password TEXT, Username TEXT)")
        # Tabla todos
        c.execute(f"""CREATE TABLE IF NOT EXISTS {todos_table} (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT,
            Description TEXT,
            Done INTEGER,
            CreateAt DATETIME DEFAULT CURRENT_TIMESTAMP,
            ModifiedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
            DueDate DATETIME DEFAULT NULL,
            UserId INTEGER,
            FOREIGN KEY(UserId) REFERENCES {users_table}(Id)
            )""")
        
        # Usamos la función get_timestamp para obtener la fecha actual + 7 días
        due_date = get_timestamp(7)
        # Conseguir lista de ids de usuarios
        c.execute(f"SELECT Id FROM {users_table}")
        users = c.fetchall()
        for user_id in users:
            # Limitamos notas a insertar
            c.execute(f"SELECT COUNT(*) FROM {todos_table} WHERE UserId = {user_id[0]}")
            todos_number = c.fetchone()[0]
            # Insertar 3 notas por cada usuario
            if todos_number < 3:
                c.execute(f"INSERT INTO todos (Title, Description, Done, DueDate, UserId) VALUES ('title1', 'description1', 0, '{due_date}', {user_id[0]})")
                # c.execute(f"INSERT INTO todos (Title, Description, Done, DueDate, UserId) VALUES ('title2', 'description2', 0, '{due_date}', {user_id[0]})")
                # c.execute(f"INSERT INTO todos (Title, Description, Done, DueDate, UserId) VALUES ('title3', 'description3', 0, '{due_date}', {user_id[0]})")
        con.commit()
        return True
    except con.Error as err:
        return err
    finally:
        con.close()

# User
# Register new user
def register_user(db_name : str, users_table : str, username : str, email : str, password : str) -> tuple[bool, str, bool] | tuple[sql.Error, None, bool]:
    """
       Registra un nuevo usuario en la base de datos.

        Args: db_name (str): nombre de la base de datos
             users_table (str): nombre de la tabla, username (str): nombre de usuario, email (str): email del usuario, password (str): contraseña del usuario
        Returns: True si el usuario se registró correctamente, False si el usuario ya existe 
                 Error si hubo un error al registrar el usuario
                 msg -> mensaje de warning
                 es_warning -> booleano que indica si es un warning o no
    """
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        # Hacemos SELECT para ver si el user existe -> email o username
        c.execute(f"SELECT * FROM {users_table} WHERE username = '{username}' OR email = '{email}'")
        account = c.fetchone() # (1, 'email@domain.com', 'password', 'pepito') # None
        es_warning = True
        if account:
            # Si el usuario ya existe, entonces no se registra
                # Se puede definir si es el username o el email lo que ya existe pero
                # a veces se deja ambiguo a propósito para evitar ataques de fuerza bruta
            msg = 'El email o username ya existen. Vuelve a intentarlo'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Email incorrecto'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'El username debe ser alfanumérico'
        elif len(password) < 5:
            # Podemos colocar varias condiciones sobre la contraseña
            # para que no sea una contraseña débil
            msg = 'La contraseña debe tener al menos 5 caracteres'
        elif not username or not password or not email:
            msg = 'Por favor, rellena todos los campos del formulario'
        else:
            # print(f'INSERT INTO {users_table} (email, password, username) VALUES (?, ?, ?)' , (email, password, username))
            c.execute(f'INSERT INTO {users_table} (Email, Password, Username) VALUES (?, ?, ?)' , (email, password, username))
            con.commit()
            msg = f'Se ha registrado correctamente el usuario: {username}'
            es_warning = False
            return (True, msg, es_warning)
    except con.Error as err:
        return (err, None, False)
    finally:
        con.close()
    return (False, msg, es_warning)

# Log user
def login_user(db_name : str, users_table : str, username : str, password : str) -> tuple[int, str, str, str] | None:
    """
        Inicia sesión de un usuario de tabla users en la base de datos.

        Args: db_name (str): bd, users_table (str): tabla users, username (str): nombre de usuario, password (str): contraseña 

        Returns: (id, email, username, password) si el usuario existe, None si no existe
    """
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        c.execute(f"SELECT * FROM {users_table} WHERE username = '{username}' AND password = '{password}'")
        account = c.fetchone() # (1, 'email@domain.com', 'password', 'pepito') o None
        if account:
            return account
    except con.Error as err:
        return (err, None, False)
    finally:
        con.close()
    return None

# Todos / Notas
# READ
# Read all todos
def read_all_todos(db_name : str, users_table : str, user_id : int) -> list[tuple] | list | sql.Error:
    """
        Lee todos los todos de un usuario en la base de datos.

        Args: db_name (str): bd, users_table (str): nombre de la tabla, user_id (int): id del usuario

        Returns: lista de todos si el usuario existe, [] si no existe o SQL Error
    """
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        c.execute(f"SELECT * FROM {users_table} WHERE UserId = {user_id}")
        todos = c.fetchall() # lista o []
        if todos:
            return todos
        return [] # Si no hay todos, entonces devuelve una lista vacía
    except con.Error as err:
        return err

# Read todo by id
def read_todo_by_id(db_name : str, users_table : str, user_id : int, todo_id : int) -> tuple | None | sql.Error:
    """
        Lee un todo de un usuario en la base de datos.

        Parámetros
        ----------
        db_name : str 
            Base de datos. 
        users_table : str 
            Nombre de la tabla.
        user_id : int 
            Id del usuario.
        todo_id : int 
            Id del todo.

        Returns 
        -------
        Tuple con el todo si el usuario existe, None si no existe o SQL Error.
    """
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        c.execute(f"SELECT * FROM {users_table} WHERE UserId = {user_id} AND Id = {todo_id}")
        todo = c.fetchone() # tuple o None
        return todo
    except con.Error as err:
        return err
    finally:
        con.close()

# WRITE
# Create new todo
def create_new_todo(db_name : str, users_table : str, user_id : int, values : list) -> tuple[bool, str] | tuple[sql.Error, None]:
    """
        Crea un nuevo todo en la base de datos.

        Args: db_name (str): bd, users_table (str): nombre de la tabla, user_id (int): id del usuario, values (list): lista con los valores del todo

        Returns: (True, 'Todo creado correctamente') si el todo se crea correctamente, SQL Error si no se crea
    """
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        
        # Usamos la función get_timestamp para obtener la fecha actual + 7 días
        due_date = get_timestamp(7)

        # validación para ver si usuario existe
            # no se realiza execute si no hay id 
            
        c.execute(f"INSERT INTO {users_table} (Title, Description, Done, DueDate, UserId) VALUES (?, ?, ?, ?, ?)", (values[0], values[1], values[2], due_date,user_id))
        con.commit()
        return (True, 'Todo creado correctamente') # posible todo: msg desde routes ?
    except con.Error as err:
        return err
    finally:
        con.close()

# Update todo
def update_todo_by_id(db_name : str, users_table : str, user_id : int, todo_id : int, values : list) -> tuple[bool, str] | tuple[sql.Error, None]:
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        # revisar
        c.execute(f"UPDATE {users_table} SET Title = {values[0]}, Description = {values[1]}, Done = {values[2]} WHERE Id = {todo_id} AND UserId = {user_id}")
        con.commit()
        return (True, f'Todo {todo_id} actualizado correctamente')
    except con.Error as err:
        return err
    finally:
        con.close()

# DELETE
# Delete todo
def delete_todo_by_id(db_name : str, users_table : str, user_id : int, todo_id : int) -> tuple[bool, str] | tuple[sql.Error, None]:
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        c.execute(f"DELETE FROM {users_table} WHERE Id = {todo_id} AND UserId = {user_id}")
        con.commit()
        return (True, f'Todo {todo_id} eliminado correctamente')
    except con.Error as err:
        return err
    finally:
        con.close()

def get_timestamp(dias : int) -> str:
    timestamp = datetime.now().timestamp()
    dt = datetime.fromtimestamp(timestamp)
    dt = dt + timedelta(days=dias)
    due_date = dt.strftime('%Y-%m-%d %H:%M:%S')
    return due_date