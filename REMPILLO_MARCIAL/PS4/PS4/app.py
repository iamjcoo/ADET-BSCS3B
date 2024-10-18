from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key' 

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'myadet'  
}

# Connect to the database
def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

# Password encryption function
def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Collect form data
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        birthdate = request.form.get('birthdate')
        email = request.form.get('email')
        address = request.form.get('address')
        password = request.form.get('password')  

        # Encrypt password
        encrypted_password = encrypt_password(password)

        # Save to MySQL database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            insert_query = '''
                INSERT INTO adet_user (first_name, middle_name, last_name, birthdate, email, address, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (first_name, middle_name, last_name, birthdate, email, address, encrypted_password))
            conn.commit()
            cursor.close()
            conn.close()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Encrypt entered password to check against the database
        encrypted_password = encrypt_password(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if user exists with the given email and password
            cursor.execute('SELECT first_name FROM adet_user WHERE email = %s AND password = %s', (email, encrypted_password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                session['user'] = user[0]  # Store user's first name in session
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid email or password.", "danger")
        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    # Fetch user details from the database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT first_name, middle_name, last_name, birthdate, email, address FROM adet_user WHERE first_name = %s', (session['user'],))
        user_details = cursor.fetchone()
        cursor.close()
        conn.close()

        return render_template('dashboard.html', user_details=user_details)
    except mysql.connector.Error as err:
        return f"Error: {err}"

@app.route('/logout')
def logout():
    session.pop('user', None)  # Clear user session
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
