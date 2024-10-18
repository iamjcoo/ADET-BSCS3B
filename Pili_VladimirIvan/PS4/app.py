from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'Adet'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '', 
    'database': 'adet'
}

def get_db():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

@app.route('/', methods = ['GET', 'POST'])
def registration():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        contact_number = request.form.get('contact_number')
        email = request.form.get('email')
        password = hashlib.sha256(request.form.get('password').encode()).hexdigest()
        
        conn = get_db()
        if conn is None:
            return "Database connection failed", 500
        
        cursor = conn.cursor()
        
        try:
            sql = '''
                INSERT INTO adet_user (first_name, middle_name, last_name, address, contact_number, email, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(sql, (first_name, middle_name, last_name, address, contact_number, email, password))
            conn.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return redirect(url_for('registration'))
        
    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = hashlib.sha256(request.form.get('password').encode()).hexdigest()

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM adet_user WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                session['email'] = email
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid credentials. Please try again.", "error")
                return redirect(url_for('login'))
        except mysql.connector.Error as e:
            flash(f"Error: {e}", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))

    user_email = session['email']
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT first_name, middle_name, last_name, contact_number, email, address FROM adet_user WHERE email = %s", (user_email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        return f"Error: {e}"

    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
    