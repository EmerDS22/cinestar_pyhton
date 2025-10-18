from flask import Flask, render_template, request
from flask_cors import CORS
from database import execute_query

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/cines.html')
def cines():
    query = "SELECT id, RazonSocial, Direccion, Detalle, Telefonos FROM vCines"
    cines_list = execute_query(query)
    
    return render_template('cines.html', cines=cines_list)

@app.route('/cine.html')
def cine():
    id_cine = request.args.get('id')

    cine_data = execute_query("SELECT * FROM vCines WHERE id = %s", (id_cine,))[0]
    tarifas = execute_query("SELECT * FROM vCineTarifas WHERE idCine = %s", (id_cine,))
    peliculas = execute_query("SELECT * FROM vCinePeliculas WHERE idCine = %s", (id_cine,))

    return render_template('cine.html', cine=cine_data, tarifas=tarifas, peliculas=peliculas)

@app.route('/peliculas.html')
def peliculas():
    estado_param = request.args.get('id')
    id_estado = 1 if estado_param == 'cartelera' else 2
    
    peliculas_list = execute_query("CALL sp_getPeliculas(%s)", (id_estado,))
    
    return render_template('peliculas.html', peliculas=peliculas_list)

@app.route('/pelicula.html')
def pelicula():
    id_pelicula = request.args.get('id')
    
    pelicula_data = execute_query("CALL sp_getPelicula(%s)", (id_pelicula,))[0]
    
    return render_template('pelicula.html', pelicula=pelicula_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)