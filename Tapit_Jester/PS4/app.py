from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# MySQL Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'adet'
}

# Establish MySQL connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Encrypt the password using SHA-256
def encrypt_password(password):
    sha_signature = hashlib.sha256(password.encode()).hexdigest()
    return sha_signature

# Register route
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
        
        # Encrypt the password before saving
        encrypted_password = encrypt_password(password)

        # Insert the data into the MySQL table
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO adet_user (first_name, middle_name, last_name, birthdate, email, address, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (first_name, middle_name, last_name, birthdate, email, address, encrypted_password)
            
            try:
                cursor.execute(insert_query, values)
                connection.commit()
                cursor.close()
                connection.close()
            except Error as e:
                print(f"Failed to insert record: {e}")
                return "Error saving data", 500

        return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Encrypt the entered password to compare with the stored one
        encrypted_password = encrypt_password(password)

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM adet_user WHERE email=%s AND password=%s", (email, encrypted_password))
            user = cursor.fetchone()

            if user:
                # Set session using email and first_name
                session['email'] = user['email']
                session['first_name'] = user['first_name']
                return redirect(url_for('dashboard'))
            else:
                return "Invalid email or password", 401

    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    email = session['email']  # Use email from session
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT first_name, middle_name, last_name, birthdate, email, address FROM adet_user WHERE email=%s", (email,))
        user_details = cursor.fetchone()

        return render_template('dashboard.html', user_details=user_details, first_name=session['first_name'])

# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
