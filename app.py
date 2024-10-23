from flask import Flask, session, redirect, url_for, request, render_template

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar sesiones en Flask

# Función para generar un ID único
def generate_id():
    return max([i['id'] for i in session.get('inscritos', [])], default=0) + 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    # Recoger datos del formulario
    fecha = request.form['fecha']
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    turno = request.form['turno']
    seminarios = request.form.getlist('seminarios')

    # Crear un nuevo registro
    inscrito = {
        'id': generate_id(),
        'fecha': fecha,
        'nombre': nombre,
        'apellidos': apellidos,
        'turno': turno,
        'seminarios': ', '.join(seminarios)  # Convertir lista a string
    }

    # Almacenar en sesión
    if 'inscritos' not in session:
        session['inscritos'] = []
    session['inscritos'].append(inscrito)
    session.modified = True  # Indicar que la sesión ha sido modificada
    return redirect(url_for('listado'))

@app.route('/listado')
def listado():
    inscritos = session.get('inscritos', [])
    return render_template('listado.html', inscritos=inscritos)

@app.route('/eliminar/<int:inscrito_id>')
def eliminar(inscrito_id):
    # Filtrar los inscritos para eliminar el registro
    session['inscritos'] = [i for i in session['inscritos'] if i['id'] != inscrito_id]
    session.modified = True
    return redirect(url_for('listado'))

@app.route('/editar/<int:inscrito_id>', methods=['POST'])
def editar(inscrito_id):
    # Buscar el registro y actualizar sus datos
    for inscrito in session['inscritos']:
        if inscrito['id'] == inscrito_id:
            inscrito['fecha'] = request.form['fecha']
            inscrito['nombre'] = request.form['nombre']
            inscrito['apellidos'] = request.form['apellidos']
            inscrito['turno'] = request.form['turno']
            inscrito['seminarios'] = ', '.join(request.form.getlist('seminarios'))  # Actualizar seminarios
            session.modified = True  # Indicar que la sesión ha sido modificada
            break
    return redirect(url_for('listado'))

if __name__ == '__main__':
    app.run(debug=True)
