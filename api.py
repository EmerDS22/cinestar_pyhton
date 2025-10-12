from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app) 

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
    results = []
    
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


@app.route('/api/cines', methods=['GET'])
def get_all_cines():
    """
    Obtiene todos los cines con su información básica.
    """
    query = """
    SELECT 
        C.id, 
        C.RazonSocial, 
        C.Salas, 
        D.Detalle AS Detalle, 
        C.Direccion, 
        C.Telefonos
    FROM Cine C
    JOIN Distrito D ON C.idDistrito = D.id
    """
    cines_list = execute_query(query)
    
    if cines_list is None:
        return jsonify(error="Error interno del servidor al consultar cines"), 500
        
    return jsonify(data=cines_list), 200


@app.route('/api/cines/<string:id_cine>', methods=['GET'])
def get_single_cine(id_cine):
    """
    Obtiene el detalle de un cine, incluyendo tarifas y películas/horarios.
    """
    cine_data = {}

    query_cine = """
    SELECT 
        C.id, C.RazonSocial, C.Direccion, 
        D.Detalle AS Distrito, C.Telefonos
    FROM Cine C
    JOIN Distrito D ON C.idDistrito = D.id
    WHERE C.id = %s
    """
    cine_result = execute_query(query_cine, (id_cine,))
    
    if cine_result is None:
        return jsonify(error="Error al consultar el cine"), 500
    if not cine_result:
        return jsonify(error="Cine no encontrado"), 404
        
    cine_data = cine_result[0]

    query_tarifas = "SELECT DiasSemana, Precio FROM CineTarifa WHERE idCine = %s"
    tarifas_result = execute_query(query_tarifas, (id_cine,))
    cine_data['tarifas'] = tarifas_result if tarifas_result is not None else []
    
    query_peliculas = """
    SELECT 
        P.Titulo, 
        CP.Horarios 
    FROM CinePelicula CP
    JOIN Pelicula P ON CP.idPelicula = P.id
    WHERE CP.idCine = %s
    """
    peliculas_result = execute_query(query_peliculas, (id_cine,))
    cine_data['peliculas'] = peliculas_result if peliculas_result is not None else []

    return jsonify(data=cine_data), 200


@app.route('/api/peliculas/<string:estado>', methods=['GET'])
def get_peliculas_by_estado(estado):
    """
    Obtiene la lista de películas filtradas por estado ('cartelera'='1' o 'estrenos'='2').
    """
    id_estado = None
    if estado == 'cartelera':
        id_estado = 1  
    elif estado == 'estrenos':
        id_estado = 2  
    else:
        return jsonify(error="Estado de película no válido."), 400

    query = """
    SELECT 
        P.id, P.Titulo, P.Sinopsis, P.Link,
        P.FechaEstreno, P.Director, P.Reparto, P.Duracion,
        getGenerosDetalle(P.Generos) as Geneross,
        DateLong(P.FechaEstreno) as FechaEstrenoss
    FROM Pelicula P
    WHERE P.idEstado = %s
    """
    
    
    peliculas_list = execute_query(query, (id_estado,))
    
    if peliculas_list is None:
        return jsonify(error="Error interno del servidor al cargar películas"), 500
        
    return jsonify(data=peliculas_list), 200


@app.route('/api/pelicula/<string:id_pelicula>', methods=['GET'])
def get_single_pelicula(id_pelicula):
    """
    Obtiene la información detallada de una película por su ID.
    """
    query = """
    SELECT 
        P.id, P.Titulo, P.Sinopsis, P.Link,
        P.FechaEstreno, P.Director, P.Reparto, P.Duracion,
        getGenerosDetalle(P.Generos) as Geneross,
        DateLong(P.FechaEstreno) as FechaEstrenoss
    FROM Pelicula P
    WHERE P.id = %s
    """
    
    pelicula_result = execute_query(query, (id_pelicula,))
    
    if pelicula_result is None:
        return jsonify(error="Error al consultar la película"), 500
    if not pelicula_result:
        return jsonify(error="Película no encontrada"), 404
        
    return jsonify(data=pelicula_result[0]), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)