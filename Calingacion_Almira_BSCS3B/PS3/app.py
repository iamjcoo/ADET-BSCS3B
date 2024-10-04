from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# MySQL database connection configuration
db_config = {
    'user': 'your_username',        # Update with your MySQL username
    'password': 'your_password',    # Update with your MySQL password
    'host': 'localhost',            # Update if your MySQL server is hosted elsewhere
    'database': 'adet',
}

# Function to save data to MySQL
def save_data_to_mysql(user_data):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Insert query
    insert_query = """
    INSERT INTO adet_user (given_name, middle_initial, surname, dob, email_address, home_address)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        user_data['given_name'],
        user_data['middle_initial'],
        user_data['surname'],
        user_data['dob'],
        user_data['email_address'],
        user_data['home_address']
    ))

    connection.commit()
    cursor.close()
    connection.close()

@app.route('/')
def homepage():
    return redirect(url_for('registration_form'))

@app.route('/register', methods=['GET', 'POST'])
def registration_form():
    if request.method == 'POST':
        # Get form input data
        given_name = request.form.get('first_name')
        middle_initial = request.form.get('middle_name')
        surname = request.form.get('last_name')
        dob = request.form.get('birthdate')
        email_address = request.form.get('email')
        home_address = request.form.get('address')

        # Data to be saved in MySQL
        user_data = {
            'given_name': given_name,
            'middle_initial': middle_initial,
            'surname': surname,
            'dob': dob,
            'email_address': email_address,
            'home_address': home_address
        }

        # Save the data to the MySQL database
        save_data_to_mysql(user_data)

        # Redirect to the success page
        return render_template('success.html')

    return render_template('registration.html')

if __name__ == '__main__':
    app.run(debug=True)