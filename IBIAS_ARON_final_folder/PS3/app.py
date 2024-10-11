from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os

app = Flask(__name__)

# Set a secret key for session management (optional, but recommended)
app.secret_key = os.urandom(24)  # Secure random key for sessions

# MySQL Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Make sure this matches your MySQL password
    'database': 'adet'
}

# Function to save data to MySQL database
def save_to_mysql(user_data):
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SQL query to insert data into adet_user table
        query = """
        INSERT INTO adet_user (first_name, middle_name, last_name, birthdate, email, address) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        # Data to be inserted
        data = (
            user_data['First Name'],
            user_data['Middle Name'],
            user_data['Last Name'],
            user_data['Birthdate'],
            user_data['Email Address'],
            user_data['Address']
        )

        # Execute the query and commit changes
        cursor.execute(query, data)
        conn.commit()

        # Print a success message
        print("Data saved successfully!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        # Close the database connection
        if conn.is_connected():
            cursor.close()
            conn.close()
    return True

@app.route('/')
def registration_form():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
    # Collect data from the form
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    birthdate = request.form['birthdate']
    email = request.form['email']
    address = request.form['address']

    # Create a dictionary of the user's data
    user_data = {
        'First Name': first_name,
        'Middle Name': middle_name,
        'Last Name': last_name,
        'Birthdate': birthdate,
        'Email Address': email,
        'Address': address
    }

    # Save the data to MySQL database and check if successful
    if save_to_mysql(user_data):
        # On success, redirect to a success page or show a message
        flash('Registration successful!', 'success')
        return redirect(url_for('registration_form'))
    else:
        # If there's an error, flash an error message
        flash('Registration failed. Please try again.', 'danger')
        return redirect(url_for('registration_form'))

if __name__ == '__main__':
    app.run(debug=True)