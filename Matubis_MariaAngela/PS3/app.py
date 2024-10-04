from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'adet'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['first-name']
        middle_initial = request.form['middle-initial']
        last_name = request.form['last-name']
        address = request.form['address']
        email_address = request.form['email-address']
        contact_number = request.form['contact-number']

        conn = get_db_connection()
        if conn is None:
            return "Database connection failed", 500

        cursor = conn.cursor()

        try:
            # Insert query to save form data into MySQL database
            insert_query = '''
                INSERT INTO adet_user (first_name, middle_initial, last_name, address, email_address, contact_number)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (first_name, middle_initial, last_name, address, email_address, contact_number))
            conn.commit()  # Commit the transaction

            # Render a welcome page with the user's name
            welcome_message = f"Hello {first_name} {last_name}, Welcome to CCS 106 - Applications Development and Emerging Technologies!"
            return render_template('welcome.html', message=welcome_message)

        except mysql.connector.Error as e:
            print(f"Error inserting data: {e}")
            return "Error inserting data into the database", 500
        finally:
            cursor.close()
            conn.close()

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
