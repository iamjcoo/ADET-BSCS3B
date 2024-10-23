from flask import Flask, render_template, request, redirect, url_for, session
import os
import mariadb
import sys
import hashlib

app = Flask(__name__)
app.secret_key = 'my_secret_key'

# Database connection function
def get_db_connection():
    try:
        conn = mariadb.connect(
            user="root",
            password="123",
            host="localhost",
            port=3306,
            database="ADETS"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    info = request.form.to_dict()
    password = info['password']
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = get_db_connection()
    cur = conn.cursor()
    sequel_query = f'INSERT INTO ADET_USERS (f_name, m_name, l_name, c_number, email, address, username, password) VALUES ("{info["f_name"]}", "{info["m_name"]}", "{info["l_name"]}", "{info["c_number"]}", "{info["email"]}", "{info["address"]}", "{info["username"]}", "{hashed_password}");'
    try:
        cur.execute(sequel_query)
        conn.commit()
    except mariadb.IntegrityError as e:
        errorData = {"Username": info["username"], "error": f'Username "{info['username']}"" already exists.'}
        return render_template('index.html', data=errorData)
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM ADET_USERS WHERE username = %s AND password = %s', (username, hashed_password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['f_name'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            errorData = {"Username": username, "error": "Invalid Username or Password"}
            return render_template('login.html', data=errorData)
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT f_name, m_name, l_name, c_number, email, address FROM ADET_USERS WHERE id = %s', (user_id,))
    user_details = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('dashboard.html', user_details=user_details)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)