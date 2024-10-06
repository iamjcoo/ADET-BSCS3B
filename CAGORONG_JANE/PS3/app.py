from flask import Flask, render_template, request, flash, redirect
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

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
            
            insert_query = '''
                INSERT INTO adet_user (first_name, middle_initial, last_name, address, email_address, contact_number)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (first_name, middle_initial, last_name, address, email_address, contact_number))
            conn.commit()

            
            flash(f"Registration successful! Welcome, {first_name} {last_name}.", "success")

            return redirect('/')  

        except mysql.connector.Error as e:
            print(f"Error inserting data: {e}")
            flash("An error occurred while registering. Please try again.", "error")
            return "Error inserting data into the database", 500
        finally:
            cursor.close()
            conn.close()

    return render_template('registration.html')

if __name__ == '__main__':
    app.run(debug=True)
