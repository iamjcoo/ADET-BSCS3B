from flask import Flask, flash, render_template, request, redirect
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Database configuration
db_config = {
    'host': 'localhost',
    'database': 'adet',
    'user': 'root',
    'password': ''
}

# Function to save data to the MySQL database
def save_to_database(user_data):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                user_data['first_name'],
                user_data['middle_name'],
                user_data['last_name'],
                user_data['contact_number'],
                user_data['email'],
                user_data['address']
            ))
            connection.commit()
            print("User data inserted successfully")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

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

    # Create a dictionary of the user's data
    user_data = {
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'contact_number': contact_number,
        'email': email,
        'address': address
    }

    # Save the data to the MySQL database
    save_to_database(user_data)

    # Flash a success message
    flash("Registration successful!", "success")

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
