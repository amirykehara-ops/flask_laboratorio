from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql
from werkzeug.security import check_password_hash, generate_password_hash
from config import DB, SECRET_KEY
from functools import wraps

app = Flask(__name__)
app.secret_key = SECRET_KEY

def get_conn():
    return pymysql.connect(host=DB['host'], port=DB['port'],
                           user=DB['user'], password=DB['password'], db=DB['db'],
                           charset=DB['charset'], cursorclass=pymysql.cursors.DictCursor)

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapped

@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('admin_panel'))
    if request.method == 'POST':
        email = request.form.get('email','').strip()
        password = request.form.get('password','').strip()
        if not email or not password:
            flash('Completa email y contraseña', 'danger')
            return render_template('login.html')
        conn = get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, nombre, email, password, rol FROM usuarios WHERE email=%s", (email,))
                user = cur.fetchone()
        finally:
            conn.close()
        if not user or not check_password_hash(user['password'], password):
            flash('Usuario o contraseña incorrectos', 'danger')
            return render_template('login.html')
        session['user_id'] = user['id']
        session['user_nombre'] = user['nombre']
        session['user_rol'] = user['rol']
        flash('Bienvenido ' + user['nombre'], 'success')
        return redirect(url_for('admin_panel'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin_panel():
    return render_template('admin.html')

@app.route('/users')
@login_required
def users_list():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nombre, email, rol FROM usuarios ORDER BY id ASC")
            users = cur.fetchall()
    finally:
        conn.close()
    return render_template('users.html', users=users)

@app.route('/users/create', methods=['GET','POST'])
@login_required
def create_user():
    if request.method == 'POST':
        nombre = request.form.get('nombre','').strip()
        email = request.form.get('email','').strip()
        password = request.form.get('password','').strip()
        rol = request.form.get('rol','usuario')
        if not nombre or not email or not password:
            flash('Rellena todos los campos obligatorios', 'danger')
            return render_template('create_user.html')
        hashed = generate_password_hash(password)
        conn = get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO usuarios (nombre,email,password,rol) VALUES (%s,%s,%s,%s)",
                            (nombre,email,hashed,rol))
            conn.commit()
            flash('Usuario creado', 'success')
            return redirect(url_for('users_list'))
        except Exception as e:
            conn.rollback()
            flash('Error: ' + str(e), 'danger')
        finally:
            conn.close()
    return render_template('create_user.html')

@app.route('/users/edit/<int:user_id>', methods=['GET','POST'])
@login_required
def edit_user(user_id):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nombre, email, rol FROM usuarios WHERE id=%s", (user_id,))
            user = cur.fetchone()
    finally:
        conn.close()
    if not user:
        flash('Usuario no encontrado', 'danger')
        return redirect(url_for('users_list'))
    if request.method == 'POST':
        nombre = request.form.get('nombre','').strip()
        email = request.form.get('email','').strip()
        password = request.form.get('password','').strip()
        rol = request.form.get('rol','usuario')
        if not nombre or not email:
            flash('Nombre y email son obligatorios', 'danger')
            return render_template('edit_user.html', user=user)
        conn = get_conn()
        try:
            with conn.cursor() as cur:
                if password:
                    hashed = generate_password_hash(password)
                    cur.execute("UPDATE usuarios SET nombre=%s, email=%s, password=%s, rol=%s WHERE id=%s",
                                (nombre,email,hashed,rol,user_id))
                else:
                    cur.execute("UPDATE usuarios SET nombre=%s, email=%s, rol=%s WHERE id=%s",
                                (nombre,email,rol,user_id))
            conn.commit()
            flash('Usuario actualizado', 'success')
            return redirect(url_for('users_list'))
        except Exception as e:
            conn.rollback()
            flash('Error: ' + str(e), 'danger')
        finally:
            conn.close()
    return render_template('edit_user.html', user=user)

@app.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if session.get('user_id') == user_id:
        flash('No puedes eliminarte a ti mismo', 'warning')
        return redirect(url_for('users_list'))
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM usuarios WHERE id=%s", (user_id,))
        conn.commit()
        flash('Usuario eliminado', 'success')
    except Exception as e:
        conn.rollback()
        flash('Error: ' + str(e), 'danger')
    finally:
        conn.close()
    return redirect(url_for('users_list'))

if __name__ == '__main__':
    app.run(debug=True)
