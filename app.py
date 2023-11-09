from flask import Flask, render_template, request, redirect, url_for, flash, session
import modules.db as mydb

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

mydb.create_table()  # Llama a la función desde el módulo

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Añade validación de campos aquí si es necesario

        # Conecta a la base de datos
        conexion = mydb.obtener_db()
        cursor = mydb.obtener_cursor(conexion)

        try:
            # Inserta los datos en la tabla 'users'
            sentencia = "INSERT INTO users (username, password) VALUES (?, ?)"
            parametros = (username, password)
            mydb.ejecutar_sentencias_con_parametros_y_commit(conexion, cursor, [sentencia], parametros)
            flash('Registro exitoso', 'success')
        except Exception as e:
            flash('Error al registrar usuario', 'danger')

        # Cierra la conexión con la base de datos
        mydb.cerrar_cursor(cursor)
        mydb.cerrar_db(conexion)

    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Realiza la autenticación comprobando la base de datos
        conexion = mydb.obtener_db()
        cursor = mydb.obtener_cursor(conexion)
        cursor.execute("SELECT username, password FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        mydb.cerrar_cursor(cursor)
        mydb.cerrar_db(conexion)

        if user:
            # Si las credenciales son válidas, inicia la sesión
            session['username'] = user[0]
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales inválidas', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return "Panel de Usuario - ¡Has iniciado sesión!"
    else:
        flash('Debes iniciar sesión primero', 'info')
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
