from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error
import hashlib

app = Flask(__name__)
app.secret_key = 'secret_key'

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='adet',  
            user='root',      
            password='1234',
            auth_plugin='mysql_native_password'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
    return None

def save_to_mysql(data):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
            sql_insert_query = """INSERT INTO adet_user(first_name, middle_name, last_name, contact_number, email_address, address, password)
                                  VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql_insert_query, (
                data['first_name'], data['middle_name'], data['last_name'],
                data['contact_number'], data['email_address'], data['address'],
                password_hash
            ))
            connection.commit()
            print("Record inserted successfully")
        except Error as e:
            print(f"Failed to insert: {e}")
        finally:
            cursor.close()
            connection.close()

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email_address = request.form['email_address']
        address = request.form['address']
        password = request.form['password']

        data = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'contact_number': contact_number,
            'email_address': email_address,
            'address': address,
            'password': password
        }

        save_to_mysql(data)
        flash("Registration successful!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_address = request.form['email_address']
        password = request.form['password']
        connection = create_connection()
        
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM adet_user WHERE email_address = %s", (email_address,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user: 
                if hashlib.sha256(password.encode()).hexdigest() == user['password']: 
                    session['user_id'] = user['id']
                    session['first_name'] = user['first_name']
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid password', 'danger') 
            else:
                flash('User not found', 'danger')  

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT first_name, middle_name, last_name, contact_number, email_address, address FROM adet_user WHERE id = %s", (session['user_id'],))
        user_details = cursor.fetchone()
        cursor.close()
        connection.close()

    return render_template('dashboard.html', user_details=user_details)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
