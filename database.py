import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'CineStar',
    'port': 3306
}

def execute_query(query, params=None):
    """
    Establece la conexión, ejecuta una consulta SQL y la cierra.
    Devuelve la lista de resultados o None en caso de error.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute(query, params or ())
        
        results = cursor.fetchall()
        return results

    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}")
        return None
        
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()