from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'secret_key' 

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='adet',  
            user='root',      
            password='1234',
            auth_plugin='mysql_native_password'  
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
    return connection

def save_to_mysql(data):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql_insert_query = """INSERT INTO adet_user (first_name, middle_name, last_name, 
                                 contact_number, email_address, address) 
                                 VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql_insert_query, (
                data['first_name'],
                data['middle_name'],
                data['last_name'],
                data['contact_number'],
                data['email_address'],
                data['address']
            ))
            connection.commit()
            print("Record inserted successfully into users table")
        except Error as e:
            print("Failed to insert into MySQL table {}".format(e))
        finally:
            cursor.close()
            connection.close()

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email_address = request.form['email_address']
        address = request.form['address']

        if not all([first_name, last_name, email_address, contact_number, address]):
            flash("All fields are required!", "danger")
            return redirect(url_for('register'))

        data = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'contact_number': contact_number,
            'email_address': email_address,
            'address': address
        }

        save_to_mysql(data)
        flash("Registration successful!", "success")
        
        return redirect(url_for('register'))

    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)
