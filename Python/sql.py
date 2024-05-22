from mysql.connector import connect
from config import host,user,password,db_name

try:
    
    connection = connect(
        host="localhost",
        user="root",
        password="1121",
        port=3306,
        database="shio",

    )
    print('Connection complete')
except Exception as ex:
    print(ex)


def get_connection():
    conection = connect(
        host=host,
        user=user,
        password=password,
        port=3306,
        database=db_name)

    cursor = conection.cursor(buffered=True)

    return conection, cursor

def cursor():
    return cursor
def change_data(query, value=None) -> None:
    connection, cursor = get_connection()
    if value is None:
        cursor.execute(query)
        connection.commit()
    else:
        cursor.execute(query, value)
        connection.commit()

    if connection.is_connected():
        connection.close()


def create_if_not_exists() -> None:
    try:
        connection, cursor = get_connection()

        cursor.execute("""CREATE TABLE IF NOT EXISTS TEST (
                       
            
            date VARCHAR(255),
            name VARCHAR(255),
            time VARCHAR(255),
            info VARCHAR(255)
            
           )""")

        connection.commit()

    except Exception as error_code:
        print("Error Base -> ", error_code)
        connection.close()
    finally:
        connection.close()

def create_if_not_exists() -> None:
    try:
        connection, cursor = get_connection()

        cursor.execute("""CREATE TABLE IF NOT EXISTS ANALYS (
                       
            
            name VARCHAR(255),
            turns VARCHAR(255)
            
           )""")

        connection.commit()

    except Exception as error_code:
        print("Error Base -> ", error_code)
        connection.close()
    finally:
        connection.close()
def fetchone(query,value = None):
    connection, cursor = get_connection()
    if value is None:
        cursor.execute(query)
    else:
        cursor.execute(query,value)
    
    result = cursor.fetchone()

    if connection.is_connected():
        connection.close()
    
    return result[0]

def fetchall(query,value = None):
    connection, cursor = get_connection()
    if value is None:
        cursor.execute(query)
    else:
        cursor.execute(query,value)
    
    result = cursor.fetchall()

    if connection.is_connected():
        connection.close()
    
    return result

if __name__ != "__main__":
    create_if_not_exists()