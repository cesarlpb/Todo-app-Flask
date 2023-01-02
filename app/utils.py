#%% utils.py
import sqlite3 as sql

# Create table if not exist
def create_table_if_not_exist(db_name : str, db_table : str):
    try:
        con = sql.connect(db_name)
        c = con.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS {db_table} (Id INTEGER PRIMARY KEY AUTOINCREMENT, Email TEXT, Password TEXT, Username TEXT)")
        con.commit()
        return True
    except con.Error as err:
        return err
    finally:
        con.close()

# Read from db functions
def read_from_db(db_name : str, db_table : str, cols : list, id : int):
    # si no recibe id, entonces devuelve todos los registros
    # si recibe id, entonces devuelve el registro con ese id
    try:
        con = sql.connect(db_name)
        c =  con.cursor()
        
        if cols == []:
            db_cols = '*'
        elif len(cols) <= 3:
            valid_cols = ['id', 'question', 'answer']
            for col in cols:
                if col.lower() not in valid_cols:
                    raise con.Error(f'{col} no es una columna válida')
            db_cols = ', '.join(cols)
        
        if id < 1:
            c.execute(f"SELECT {db_cols} FROM {db_table}")
            questions = c.fetchall()
            return questions
        else:
            c.execute(f"SELECT {db_cols} FROM {db_table} WHERE id = {id}")
            question = c.fetchone()
            return question
    except con.Error as err: # if error
        return err
    finally:
        # Todo: pasar a una función aparte para determinar dinámicamente las columnas
        # data = c.execute(f"SELECT * FROM {db_table}")
        # cols = []
        # for column in data.description:
        #     cols.append(column[0])
        # print(cols)
        con.close()

# Write to db functions
def write_to_db(db_name : str, db_table : str, values : list[str, str]):
    # INSERT no necesita id porque es autoincremental
    try:
        con = sql.connect(db_name)
        if len(values) != 2:
            raise con.Error('Se requieren 2 valores')
        elif not values[0] or not values[1]:
            raise con.Error('No se pueden insertar valores vacíos')
        else:
            try:
                db_values = f"'{values[0]}', '{values[1]}'"
            except TypeError as err:
                return err
        c =  con.cursor() # cursor
        print(f"INSERT INTO {db_table} (Question, Answer) VALUES ({db_values})")
        c.execute(f"INSERT INTO {db_table} (Question, Answer) VALUES ({db_values})")
        con.commit() # apply changes
        return True
    except con.Error as err: # if error
        return err
    finally:
        con.close() # close the connection
# Update db functions
def update_db(db_name : str, db_table : str, values : list[str, str], id : int):
    # id es requerido
    is_valid_id = bool(read_from_db(db_name, db_table, ["Id"], id)) # True if id exists, False otherwise
    if not is_valid_id:
        return False
    else:
        try:
            con = sql.connect(db_name)
            c =  con.cursor() # cursor
            c.execute(f"UPDATE {db_table} SET Question='{values[0]}', Answer='{values[1]}' WHERE id = {id}")
            con.commit() # apply changes
            return True 
        except con.Error as err: # if error
            return err
        finally:
            con.close() # close the connection
# Delete from db functions
def delete_from_db(db_name : str, db_table : str, id : int):
    # Id es requerido
    try:
        con = sql.connect(db_name)
        c =  con.cursor()
        c.execute(f"DELETE FROM {db_table} WHERE id = {id}")
        con.commit()
        return True
    except con.Error as err:
        return err
    finally:
        con.close()
# %%