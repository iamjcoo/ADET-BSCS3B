from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',   
    'password': '',  
    'database': 'adet'
}

# Connect to the database
def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Collect form data
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        birthdate = request.form.get('birthdate')
        email = request.form.get('email')
        address = request.form.get('address')

        # Save to MySQL database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            insert_query = '''
                INSERT INTO adet_user (first_name, middle_name, last_name, birthdate, email, address)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (first_name, middle_name, last_name, birthdate, email, address))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('success'))
        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template('register.html')

@app.route('/success')
def success():
    return "Registration Successful!"

if __name__ == '__main__':
    app.run(debug=True)
