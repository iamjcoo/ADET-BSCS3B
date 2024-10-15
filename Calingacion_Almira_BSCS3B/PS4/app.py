from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import hashlib  # For SHA-256 encryption
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# MySQL database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'adet'
}

# Function to save data to MySQL
def save_data_to_mysql(user_data):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Insert query for registration
    insert_query = """
    INSERT INTO adet_user (first_name, middle_name, last_name, birthdate, email, address, password)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        user_data['first_name'],
        user_data['middle_name'],
        user_data['last_name'],
        user_data['birthdate'],
        user_data['email'],
        user_data['address'],
        user_data['password']  # Already hashed before insertion
    ))

    connection.commit()
    cursor.close()
    connection.close()

# Function to check if email already exists in the database
def email_exists(email):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT email FROM adet_user WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result is not None

# Function to verify login
def verify_login(email, password):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    # Query to get the user's hashed password from the database
    cursor.execute("SELECT * FROM adet_user WHERE email = %s", (email,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    # If user exists and the password matches, return user data
    if user and user['password'] == hashlib.sha256(password.encode()).hexdigest():
        return user
    return None

@app.route('/')
def homepage():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def registration_form():
    if request.method == 'POST':
        # Get form input data
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        birthdate = request.form.get('birthdate')
        email = request.form.get('email')
        address = request.form.get('address')
        password = request.form.get('password')

        # Check if the email is already registered
        if email_exists(email):
            flash('Email is already registered. Please log in.', 'error')
            return redirect(url_for('login'))

        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Data to be saved in MySQL
        user_data = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'birthdate': birthdate,
            'email': email,
            'address': address,
            'password': hashed_password
        }

        # Save the data to the MySQL database
        save_data_to_mysql(user_data)

        # Redirect to the success page
        return render_template('success.html')

    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Verify login credentials
        user = verify_login(email, password)

        if user:
            # Set session variables
            session['logged_in'] = True
            session['email'] = user['email']
            session['first_name'] = user['first_name']

            # Redirect to the dashboard
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Ensure user is logged in
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Fetch user details except the password
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT first_name, middle_name, last_name, birthdate, email, address FROM adet_user WHERE email = %s", (session['email'],))
    user_details = cursor.fetchone()
    cursor.close()
    connection.close()

    # Render the dashboard template with user details
    return render_template('dashboard.html', first_name=session['first_name'], user_details=user_details)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
