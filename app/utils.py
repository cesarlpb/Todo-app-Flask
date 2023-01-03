#%% utils.py
import sqlite3 as sql
import re

# Create table if not exist
def create_tables_if_not_exist(db_name : str, db_table : str, todos_table : str) -> bool | sql.Error:
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        # Start a transaction
        c.execute('BEGIN')
        c.execute(f"CREATE TABLE IF NOT EXISTS {db_table} (Id INTEGER PRIMARY KEY AUTOINCREMENT, Email TEXT, Password TEXT, Username TEXT)")
        # c.execute(f"CREATE TABLE IF NOT EXISTS {todos_table} (Id INTEGER PRIMARY KEY AUTOINCREMENT,Title TEXT,Description TEXT,Done INTEGER,CreateAt DATETIME DEFAULT CURRENT_TIMESTAMP,ModifiedAt DATETIME DEFAULT CURRENT_TIMESTAMP,DueDate DATETIME DEFAULT CURRENT_TIMESTAMP,UserId INTEGER,FOREIGN KEY(UserId) REFERENCES {db_table}(Id)")
        
        # revisar - DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 1 DAY)

        c.execute("""CREATE TABLE IF NOT EXISTS todos (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT,
            Description TEXT,
            Done INTEGER,
            CreateAt DATETIME DEFAULT CURRENT_TIMESTAMP,
            ModifiedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
            DueDate DATETIME DEFAULT CURRENT_TIMESTAMP,
            UserId INTEGER,
            FOREIGN KEY(UserId) REFERENCES users(Id)
            )""")

        # c.execute("INSERT INTO todos (Title, Description, Done, UserId) VALUES ('title11', 'description11', 0, 1)")
        
        # c.execute("INSERT INTO todos (Title, Description, Done, UserId) VALUES ('title21', 'description21', 0, 2)")
        # c.execute("INSERT INTO todos (Title, Description, Done, UserId) VALUES ('title31', 'description31', 0, 3)")
            # todo: hay que limitar la inserción de datos para que solo haya cierta cantidad de todos... 5-10 todos por usuario

        # c.execute(f"CREATE TABLE IF NOT EXISTS {todos_table} (Id INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT, Description TEXT, Done INTEGER, CreateAt DEFAULT CURRENT_TIMESTAMP, ModifiedAt DEFAULT CURRENT_TIMESTAMP, DueDate DATETIME DEFAULT DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 1 DAY), UserId INTEGER, FOREIGN KEY(UserId) REFERENCES {db_table}(Id))")
        con.commit()
        return True
    except con.Error as err:
        return err
    finally:
        con.close()

# Register new user
def register_user(db_name : str, db_table : str, username : str, email : str, password : str) -> tuple[bool, str, bool] | tuple[sql.Error, None, bool]:
    """
       Registra un nuevo usuario en la base de datos.

        Args: db_name (str): nombre de la base de datos
             db_table (str): nombre de la tabla, username (str): nombre de usuario, email (str): email del usuario, password (str): contraseña del usuario
        Returns: True si el usuario se registró correctamente, False si el usuario ya existe 
                 Error si hubo un error al registrar el usuario
                 msg -> mensaje de warning
                 es_warning -> booleano que indica si es un warning o no
    """
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        # Hacemos SELECT para ver si el user existe -> email o username
        c.execute(f"SELECT * FROM {db_table} WHERE username = '{username}' OR email = '{email}'")
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
            # print(f'INSERT INTO {db_table} (email, password, username) VALUES (?, ?, ?)' , (email, password, username))
            c.execute(f'INSERT INTO {db_table} (Email, Password, Username) VALUES (?, ?, ?)' , (email, password, username))
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
def login_user(db_name : str, db_table : str, username : str, password : str) -> tuple[int, str, str, str] | None:
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        c.execute(f"SELECT * FROM {db_table} WHERE username = '{username}' AND password = '{password}'")
        account = c.fetchone() # (1, 'email@domain.com', 'password', 'pepito') # None
        if account:
            return account
    except con.Error as err:
        return (err, None, False)
    finally:
        con.close()
    return None

# Read from db functions
def read_all_todos(db_name : str, db_table : str, user_id : int) -> list[tuple] | list | sql.Error:
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        c.execute(f"SELECT * FROM {db_table} WHERE UserId = {user_id}")
        todos = c.fetchall() # lista o []
        if todos:
            return todos
        return [] # Si no hay todos, entonces devuelve una lista vacía
    except con.Error as err:
        return err

def read_todo_by_id(db_name : str, db_table : str, user_id : int, todo_id : int) -> tuple | None | sql.Error:
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        c.execute(f"SELECT * FROM {db_table} WHERE UserId = {user_id} AND Id = {todo_id}")
        todo = c.fetchone() # tuple o None
        return todo
    except con.Error as err:
        return err
    finally:
        con.close()
    
# def read_from_db(db_name : str, db_table : str, cols : list, id : int):
#     # si no recibe id, entonces devuelve todos los registros
#     # si recibe id, entonces devuelve el registro con ese id
#     try:
#         con = sql.connect(db_name)
#         c =  con.cursor()
        
#         if cols == []:
#             db_cols = '*'
#         elif len(cols) <= 3:
#             valid_cols = ['id', 'question', 'answer']
#             for col in cols:
#                 if col.lower() not in valid_cols:
#                     raise con.Error(f'{col} no es una columna válida')
#             db_cols = ', '.join(cols)
        
#         if id < 1:
#             c.execute(f"SELECT {db_cols} FROM {db_table}")
#             questions = c.fetchall()
#             return questions
#         else:
#             c.execute(f"SELECT {db_cols} FROM {db_table} WHERE id = {id}")
#             question = c.fetchone()
#             return question
#     except con.Error as err: # if error
#         return err
#     finally:
#         # Todo: pasar a una función aparte para determinar dinámicamente las columnas
#         # data = c.execute(f"SELECT * FROM {db_table}")
#         # cols = []
#         # for column in data.description:
#         #     cols.append(column[0])
#         # print(cols)
#         con.close()

# Write to db functions
    # create todo
def create_new_todo(db_name : str, db_table : str, user_id : int, values : list) -> tuple[bool, str] | tuple[sql.Error, None]:
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        c.execute(f"INSERT INTO {db_table} (Title, Description, Done, UserId) VALUES (?, ?, ?, ?)", (values[0], values[1], values[2], user_id))
        con.commit()
        return (True, 'Todo creado correctamente')
    except con.Error as err:
        return err
    finally:
        con.close()

# Update todo
def update_todo_by_id(db_name : str, db_table : str, user_id : int, todo_id : int, values : list) -> tuple[bool, str] | tuple[sql.Error, None]:
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        # print(f"UPDATE {db_table} SET Title = {values[0]}, Description = {values[1]}, Done = {values[2]} WHERE Id = {todo_id} AND UserId = {user_id}")
        # c.execute(f"UPDATE {db_table} SET Title = ?, Description = ?, Done = ? WHERE Id = ? AND UserId = ?", (values[0], values[1], values[2], todo_id, user_id))
        c.execute(f"UPDATE {db_table} SET Title = {values[0]}, Description = {values[1]}, Done = {values[2]} WHERE Id = {todo_id} AND UserId = {user_id}")
        con.commit()
        return (True, f'Todo {todo_id} actualizado correctamente')
    except con.Error as err:
        return err
    finally:
        con.close()

# Delete todo
def delete_todo_by_id(db_name : str, db_table : str, user_id : int, todo_id : int) -> tuple[bool, str] | tuple[sql.Error, None]:
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        c.execute(f"DELETE FROM {db_table} WHERE Id = {todo_id} AND UserId = {user_id}")
        con.commit()
        return (True, f'Todo {todo_id} eliminado correctamente')
    except con.Error as err:
        return err
    finally:
        con.close()