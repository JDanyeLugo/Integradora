import mysql.connector
from flask import Flask, render_template, request, redirect, url_for,flash

app = Flask(__name__)
app.secret_key = 'MY SECRET KEY'

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
    'password': '',
    'database': 'creciendo'
}

def conectar_db():
    return mysql.connector.connect(**db_config)

@app.route('/eliminar_cliente/<int:id>', methods=['POST'])
def eliminar_cliente(id):
    try:
        db = conectar_db()
        cursor = db.cursor()

        cursor.execute('DELETE FROM clientes WHERE ID_Cliente = %s', (id,))
        db.commit()

        cursor.close()
        db.close()

        flash('Cliente eliminado exitosamente', 'success')

    except mysql.connector.Error as err:
        flash('Error al eliminar el cliente', 'error')

    return redirect(url_for('clientes'))

if __name__ == '__main__':
    app.run(debug=True)
