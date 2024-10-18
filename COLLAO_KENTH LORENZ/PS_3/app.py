from flask import Flask, render_template, request, flash
import mysql.connector
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random key for sessions

# MySQL Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'adet'
}

def create_db_connection():
    """Establish and return a MySQL database connection."""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def save_to_mysql(user_data):
    """Save user data to the adet_user table in MySQL database."""
    conn = create_db_connection()
    if not conn:
        print("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO adet_user (first_name, middle_name, last_name, birthdate, email, address) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        data = (
            user_data['first_name'],
            user_data['middle_name'],
            user_data['last_name'],
            user_data['birthdate'],
            user_data['email'],
            user_data['address']
        )
        cursor.execute(query, data)
        conn.commit()
        print("User data saved successfully.")

    except mysql.connector.Error as err:
        print(f"Error saving data: {err}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/')
def registration_form():
    """Render the registration form."""
    return render_template('index.html', success=False)

@app.route('/register', methods=['POST'])
def register():
    """Handle form submission and save data to the database."""
    user_data = {
        'first_name': request.form['first_name'],
        'middle_name': request.form['middle_name'],
        'last_name': request.form['last_name'],
        'birthdate': request.form['birthdate'],
        'email': request.form['email'],
        'address': request.form['address']
    }

    # Save the user data and flash a success message
    save_to_mysql(user_data)
    flash('Registration successful!', 'success')

    # Re-render the form with the success flag
    return render_template('index.html', success=True)

if __name__ == '__main__':
    app.run(debug=True)
