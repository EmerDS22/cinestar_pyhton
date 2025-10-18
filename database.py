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
    Ejecuta una consulta SQL genérica (para vistas o SELECTs simples).
    Devuelve la lista de resultados.
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

def call_procedure(proc_name, params=None):
    """
    Llama a un procedimiento almacenado usando callproc.
    Devuelve la lista de resultados del primer conjunto de resultados.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        
        cursor.callproc(proc_name, params or [])
        
        results = []
        for result in cursor.stored_results():
            results = result.fetchall()
            break 
            
        return results

    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}")
        return None
        
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()