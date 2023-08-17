import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
           
            db = mysql.connector.connect(
                host='localhost',
                user='root',  
                password='',  
                database='creciendo'
            )
            cursor = db.cursor(dictionary=True)

            cursor.execute('SELECT * FROM administrador WHERE Usuario = %s', (username,))
            user = cursor.fetchone()

            if user is None:
                error = 'Ingrese Datos Validos'
            else:
                return redirect(url_for('deshboard'))
        
        except mysql.connector.Error as err:
            error = 'Error connecting to the database. Please check your credentials.'

    return render_template('login.html', error=error)

@app.route('/deshboard')
def deshboard():
    return render_template('deshboard.html')

@app.route('/clientes')
def clientes():
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='creciendo'
        )
        cursor = db.cursor()

        cursor.execute('SELECT * FROM clientes')
        clientes = cursor.fetchall()

        cursor.close()
        db.close()

    except mysql.connector.Error as err:
        return f'Error al acceder a la base de datos: {err}'

    return render_template('clientes.html', clientes=clientes)

# ...

@app.route('/agregar_cliente', methods=['GET', 'POST'])
def agregar_cliente():
    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        nueva_direccion = request.form['direccion']
        nuevo_telefono = request.form['telefono']
        nuevo_email = request.form['email']
        
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='creciendo'
            )
            cursor = db.cursor()

            cursor.execute('INSERT INTO clientes (Nombre, Direccion, Telefono, Email) VALUES (%s, %s, %s, %s)',
                           (nuevo_nombre, nueva_direccion, nuevo_telefono, nuevo_email))
            db.commit()

            cursor.close()
            db.close()

            return redirect(url_for('clientes'))

        except mysql.connector.Error as err:
            return f'Error al agregar el cliente: {err}'

    return render_template('agregar_cliente.html')

# ...
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'creciendo'
}

def conectar_db():
    return mysql.connector.connect(**db_config)

@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        nueva_direccion = request.form['direccion']
        nuevo_telefono = request.form['telefono']
        nuevo_email = request.form['email']
        
        try:
            db = mysql.connector.connect(**db_config)
            
            cursor = db.cursor()

            cursor.execute('UPDATE clientes SET Nombre=%s, Direccion=%s, Telefono=%s, Email=%s WHERE ID_Cliente=%s',
                           (nuevo_nombre, nueva_direccion, nuevo_telefono, nuevo_email, id))
            db.commit()

            cursor.close()
            db.close()

            return redirect(url_for('clientes')) 

        except mysql.connector.Error as err:
            return f'Error al actualizar el cliente: {err}'

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        cursor.execute('SELECT * FROM clientes WHERE ID_Cliente = %s', (id,))
        cliente = cursor.fetchone()

        cursor.close()
        db.close()

        return render_template('editar_cliente.html', cliente=cliente, id_cliente=id)

    except mysql.connector.Error as err:
        return f'Error al obtener el cliente: {err}'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password':'',
    'database': 'creciendo'
}

def conectar_db():
    return mysql.connector.connect(**db_config)

@app.route('/eliminar_cliente/<int:id>', methods=['POST'])
def eliminar_cliente(id):
    try:
        db = conectar_db()
        cursor = db.cursor()

        # Verificar si el cliente tiene datos relacionados en las tablas
        cursor.execute('SELECT COUNT(*) FROM prestamos WHERE ID_Cliente = %s', (id,))
        num_prestamos = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM pagos WHERE ID_Cliente = %s', (id,))
        num_pagos = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM reportes WHERE ID_Cliente = %s', (id,))
        num_reportes = cursor.fetchone()[0]

        if num_prestamos > 0 or num_pagos > 0 or num_reportes > 0:
            flash('No se puede eliminar el cliente porque tiene datos relacionados en otras tablas.', 'error')
        else:
            cursor.execute('DELETE FROM clientes WHERE ID_Cliente = %s', (id,))
            db.commit()
            flash('Cliente eliminado exitosamente', 'success')

        cursor.close()
        db.close()

    except mysql.connector.Error as err:
        flash('Error al eliminar el cliente', 'error')

    return redirect(url_for('clientes')) 

#...
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'creciendo'
}

def conectar_db():
    return mysql.connector.connect(**db_config)

# Ruta para mostrar todos los préstamos
@app.route('/prestamos')
def prestamos():
    try:
        db = conectar_db()
        cursor = db.cursor()

        cursor.execute('SELECT * FROM prestamos')
        prestamos = cursor.fetchall()

        cursor.close()
        db.close()

    except mysql.connector.Error as err:
        return f'Error al acceder a la base de datos: {err}'

    return render_template('prestamos.html', prestamos=prestamos)

# Ruta para agregar un préstamo
@app.route('/agregar_prestamo', methods=['GET', 'POST'])
def agregar_prestamo():
    if request.method == 'POST':
        nuevo_monto = request.form['monto']
        nueva_tasa = request.form['tasa']
        nueva_fecha_inicio = request.form['fecha_inicio']
        nueva_fecha_vencimiento = request.form['fecha_vencimiento']
        nuevo_estado = request.form['estado']

        try:
            db = conectar_db()
            cursor = db.cursor()

            cursor.execute('INSERT INTO prestamos (Monto, TasaInteres, FechaInicio, FechaVencimiento, Estado) VALUES (%s, %s, %s, %s, %s)',
                           (nuevo_monto, nueva_tasa, nueva_fecha_inicio, nueva_fecha_vencimiento, nuevo_estado))
            db.commit()

            cursor.close()
            db.close()

            return redirect(url_for('prestamos'))

        except mysql.connector.Error as err:
            return f'Error al agregar el préstamo: {err}'

    return render_template('agregar_prestamo.html')

# Ruta para editar un préstamo
@app.route('/editar_prestamo/<int:id>', methods=['GET', 'POST'])
def editar_prestamo(id):
    if request.method == 'POST':
        nuevo_monto = request.form['monto']
        nueva_tasa = request.form['tasa']
        nueva_fecha_inicio = request.form['fecha_inicio']
        nueva_fecha_vencimiento = request.form['fecha_vencimiento']
        nuevo_estado = request.form['estado']

        try:
            db = conectar_db()
            cursor = db.cursor()

            cursor.execute('UPDATE prestamos SET Monto=%s, TasaInteres=%s, FechaInicio=%s, FechaVencimiento=%s, Estado=%s WHERE ID_Prestamo=%s',
                           (nuevo_monto, nueva_tasa, nueva_fecha_inicio, nueva_fecha_vencimiento, nuevo_estado, id))
            db.commit()

            cursor.close()
            db.close()

            return redirect(url_for('prestamos'))

        except mysql.connector.Error as err:
            flash('Error al actualizar el préstamo', 'error')

    try:
        db = conectar_db()
        cursor = db.cursor()

        cursor.execute('SELECT * FROM prestamos WHERE ID_Prestamo = %s', (id,))
        prestamo = cursor.fetchone()

        cursor.close()
        db.close()

        return render_template('editar_prestamo.html', prestamo=prestamo, id_prestamo=id)

    except mysql.connector.Error as err:
        flash('Error al obtener el préstamo', 'error')

    return redirect(url_for('prestamos'))

# Ruta para eliminar un préstamo
@app.route('/eliminar_prestamo/<int:id>', methods=['POST'])
def eliminar_prestamo(id):
    try:
        db = conectar_db()
        cursor = db.cursor()

        cursor.execute('DELETE FROM prestamos WHERE ID_Prestamo = %s', (id,))
        db.commit()
        flash('Préstamo eliminado exitosamente', 'success')

        cursor.close()
        db.close()

    except mysql.connector.Error as err:
        flash('Error al eliminar el préstamo', 'error')

    return redirect(url_for('prestamos'))
    
if __name__ == '__main__':
    app.run(debug=True)
