from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'adet'   
}

# Establish MySQL connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Register route
@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Collect form data00
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        birthdate = request.form.get('birthdate')
        email = request.form.get('email')
        address = request.form.get('address')

        # Insert the data into the MySQL table
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO adet_user (first_name, middle_name, last_name, birthdate, email, address)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (first_name, middle_name, last_name, birthdate, email, address)
            
            try:
                cursor.execute(insert_query, values)
                connection.commit()
                cursor.close()
                connection.close()
            except Error as e:
                print(f"Failed to insert record: {e}")
                return "Error saving data", 500

        return redirect(url_for('success'))

    return render_template('register.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)