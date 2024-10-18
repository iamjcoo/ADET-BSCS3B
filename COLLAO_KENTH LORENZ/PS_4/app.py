from flask import Flask, render_template, request, redirect, session, flash, url_for
import mysql.connector
import os
from hashlib import sha256

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = os.urandom(24)  # Secure random key for sessions

# MySQL Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'adet'
}

# Function to save user data with encrypted password to MySQL database
def save_to_mysql(user_data):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insert user data into the users table
        query = "INSERT INTO users (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, user_data)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Route: Home/Registration Page
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']

        # Encrypt the password using SHA-256
        encrypted_password = sha256(password.encode()).hexdigest()

        # Save user data to the database
        save_to_mysql((first_name, last_name, username, encrypted_password))

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

# Route: Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Encrypt the entered password to compare with the stored hash
        encrypted_password = sha256(password.encode()).hexdigest()

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # Query to check if the user exists
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, encrypted_password))
            user = cursor.fetchone()

            if user:
                session['user_id'] = user['id']
                session['first_name'] = user['first_name']
                flash('Login successful!')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials. Please try again.')
        finally:
            cursor.close()
            conn.close()

    return render_template('login.html')

# Route: Dashboard (Protected Page)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('login'))

    first_name = session['first_name']

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch user details except password
        query = "SELECT id, first_name, last_name, username FROM users WHERE id = %s"
        cursor.execute(query, (session['user_id'],))
        user_details = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

    return render_template('dashboard.html', first_name=first_name, user_details=user_details)

# Route: Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
