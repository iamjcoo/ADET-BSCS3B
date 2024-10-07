from flask import Flask, render_template, request, flash, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'adet'
}

def get_db_connection():
    """Establish and return a connection to the database."""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    """Handle registration and display the registration form."""
    if request.method == 'POST':
        # Get form data
        first_name = request.form['first-name']
        middle_initial = request.form['middle-initial']
        last_name = request.form['last-name']
        address = request.form['address']
        email_address = request.form['email-address']
        contact_number = request.form['contact-number']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match. Please try again.", "error")
            return render_template('index.html')

        # Hash the password for secure storage
        hashed_password = generate_password_hash(password)

        # Establish a DB connection
        conn = get_db_connection()
        if conn is None:
            return "Database connection failed", 500

        cursor = conn.cursor()

        try:
            # Insert query to save form data into the MySQL database
            insert_query = '''
                INSERT INTO adet_user (first_name, middle_initial, last_name, address, email_address, contact_number, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (first_name, middle_initial, last_name, address, email_address, contact_number, hashed_password))
            conn.commit()  # Commit the transaction

            # Redirect to the login page after successful registration
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))  # Changed to redirect to login page
        except mysql.connector.Error as e:
            print(f"Error inserting data: {e}")
            return "Error inserting data into the database", 500
        finally:
            cursor.close()
            conn.close()

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle the login logic."""
    if request.method == 'POST':
        # Get the email and password from the form
        email_address = request.form['email-address']
        password = request.form['password']

        # Establish a DB connection
        conn = get_db_connection()
        if conn is None:
            return "Database connection failed", 500

        cursor = conn.cursor(dictionary=True)

        try:
            # Retrieve the user's data based on email
            query = "SELECT * FROM adet_user WHERE email_address = %s"
            cursor.execute(query, (email_address,))
            user = cursor.fetchone()

            # Check if user exists
            if user is None:
                flash("Invalid email address or password.", "error")
                return render_template('login.html')

            # Verify the password
            if check_password_hash(user['password'], password):
                # Successful login
                welcome_message = (f"Hello! {user['first_name']} {user['middle_initial']}. {user['last_name']}, "
                                   f"Welcome to CCS 106 - Applications Development and Emerging Technologies! "
                                   f"Your registered email is {user['email_address']}, "
                                   f"your contact number is {user['contact_number']}, "
                                   f"and you are from {user['address']}.")
                return render_template('welcome.html', message=welcome_message)
            else:
                flash("Invalid email address or password.", "error")
                return render_template('login.html')

        except mysql.connector.Error as e:
            print(f"Error fetching data: {e}")
            return "Error logging in", 500
        finally:
            cursor.close()  # Ensure cursor is closed
            conn.close()    # Ensure connection is closed

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
