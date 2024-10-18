from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session management

# Path to SQLite database file
DATABASE = 'adet.db'

# Function to initialize the SQLite database and create the table if it doesn't exist
def init_sqlite_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS adet_user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            middle_name TEXT,
            last_name TEXT NOT NULL,
            contact_number TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            address TEXT NOT NULL,
            password TEXT NOT NULL,
            message TEXT DEFAULT ''  -- New column for custom message
        )
    ''')

    conn.commit()
    conn.close()

# Call the function to initialize the database
init_sqlite_db()

# Function to save data to SQLite
def save_to_sqlite(data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Insert query
    cursor.execute('''
        INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address, password)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['first_name'], data['middle_name'], data['last_name'],
        data['contact_number'], data['email'], data['address'], data['password']
    ))

    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Email and password are required!")
            return redirect(url_for('login'))

        # Encrypt the password to compare
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check credentials in the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM adet_user WHERE email=? AND password=?
        ''', (email, hashed_password))

        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]  # Save user ID to session
            session['first_name'] = user[1]  # Save first name to session
            return redirect(url_for('dashboard'))
        else:
            flash("Incorrect email or password.")  # Show an error message
            return redirect(url_for('login'))

    return render_template('index.html')
@app.route('/add_message', methods=['POST'])
def add_message():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    message = request.form.get('message')
    
    # Save the message for the logged-in user
    user_id = session['user_id']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Update the message for the specific user
    cursor.execute('UPDATE adet_user SET message = ? WHERE id = ?', (message, user_id))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        contact_number = request.form.get('contact_number')
        email = request.form.get('email')
        address = request.form.get('address')
        password = request.form.get('password')

        if not (first_name and last_name and contact_number and email and address and password):
            return "All fields are required", 400

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Save form data to SQLite
        form_data = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'contact_number': contact_number,
            'email': email,
            'address': address,
            'password': hashed_password
        }
        save_to_sqlite(form_data)

        return redirect(url_for('success'))

    return render_template('register.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT first_name, email, message FROM adet_user')
    users = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html', users=users)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('first_name', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
