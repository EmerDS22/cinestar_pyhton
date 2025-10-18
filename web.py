from flask import Flask, render_template, request
from database import call_procedure, execute_query

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('home.html')

@app.route('/cines.html')
def cines():
    cines_list = call_procedure('sp_getCines')
    
    return render_template('cines.html', cines=cines_list)

@app.route('/cine.html')
def cine():
    id_cine = request.args.get('id')

    cine_data = call_procedure('sp_getCine', [id_cine])[0]
    tarifas = call_procedure('sp_getCineTarifas', [id_cine])
    peliculas = call_procedure('sp_getCinePeliculas', [id_cine])

    return render_template('cine.html', cine=cine_data, tarifas=tarifas, peliculas=peliculas)

@app.route('/peliculas.html')
def peliculas():
    estado_param = request.args.get('id')
    id_estado = 1 if estado_param == 'cartelera' else 2
    
    peliculas_list = call_procedure('sp_getPeliculas', [id_estado])
    
    return render_template('peliculas.html', peliculas=peliculas_list)

@app.route('/pelicula.html')
def pelicula():
    id_pelicula = request.args.get('id')
    
    pelicula_data = call_procedure('sp_getPelicula', [id_pelicula])[0]
    
    return render_template('pelicula.html', pelicula=pelicula_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)