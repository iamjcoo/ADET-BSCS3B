from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

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
            email TEXT NOT NULL,
            address TEXT NOT NULL
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
        INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data['first_name'], data['middle_name'], data['last_name'],
        data['contact_number'], data['email'], data['address']
    ))

    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        contact_number = request.form.get('contact_number')
        email = request.form.get('email')
        address = request.form.get('address')

        if not (first_name and last_name and contact_number and email and address):
            return "All fields are required", 400

        # Save form data to SQLite
        form_data = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'contact_number': contact_number,
            'email': email,
            'address': address
        }
        save_to_sqlite(form_data)

        return redirect(url_for('success'))

    return render_template('index.html')

@app.route('/success')
def success():
    return "Registration successful!"

if __name__ == '__main__':
    app.run(debug=True)
