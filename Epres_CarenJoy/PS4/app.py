from flask import Flask, flash, render_template, request, redirect, session
import mysql.connector
from mysql.connector import Error
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Database configuration
db_config = {
    'host': 'localhost',
    'database': 'adet',
    'user': 'root',
    'password': ''
}

# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Function to save data to the MySQL database
def save_to_database(user_data):
    try:
        connection = get_db_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                user_data['first_name'],
                user_data['middle_name'],
                user_data['last_name'],
                user_data['contact_number'],
                user_data['email'],
                user_data['address'],
                user_data['password']
            ))
            connection.commit()
            print("User data inserted successfully")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to check user credentials during login
def check_user_credentials(email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        connection = get_db_connection()
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            select_query = "SELECT * FROM adet_user WHERE email = %s AND password = %s"
            cursor.execute(select_query, (email, hashed_password))
            return cursor.fetchone()  # Returns user data if credentials are valid
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return None

@app.route('/')
def registration_form():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
    # Collect data from the form
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    contact_number = request.form['contact_number']
    email = request.form['email']
    address = request.form['address']
    password = request.form['password']

    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Create a dictionary of the user's data
    user_data = {
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'contact_number': contact_number,
        'email': email,
        'address': address,
        'password': hashed_password
    }

    # Save the data to the MySQL database
    save_to_database(user_data)

    # Flash a success message
    flash("Registration successful! Please log in.", "success")

    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = check_user_credentials(email, password)

        if user:
            session['user'] = {
                'first_name': user['first_name'],
                'middle_name': user['middle_name'],
                'last_name': user['last_name'],
                'contact_number': user['contact_number'],
                'email': user['email'],
                'address': user['address']
            }
            return redirect('/dashboard')
        else:
            flash("Invalid email or password", "danger")
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    
    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
