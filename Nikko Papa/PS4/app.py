import json
import hashlib
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin123',
    'database': 'adet'
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = {
            'first_name': request.form.get('first_name'),
            'middle_name': request.form.get('middle_name'),
            'last_name': request.form.get('last_name'),
            'contact_number': request.form.get('contact_number'),
            'email': request.form.get('email'),
            'address': request.form.get('address'),
            'password': hashlib.sha256(request.form.get('password').encode()).hexdigest()  # Encrypt password
        }
        
        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (data['first_name'], data['middle_name'], data['last_name'], data['contact_number'], data['email'], data['address'], data['password'])
            )
            db.commit()
            flash('Registration successful! Please log in.', 'success')
        except Error as e:
            flash(f'Error occurred: {e}', 'danger')
        finally:
            if db.is_connected():
                cursor.close()
                db.close()
        return redirect(url_for('home'))
    
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = hashlib.sha256(request.form.get('password').encode()).hexdigest()  # Encrypt password
        
        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("SELECT first_name FROM adet_user WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
            
            if user:
                session['first_name'] = user[0]
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials. Please try again.', 'danger')
        except Error as e:
            flash(f'Error occurred: {e}', 'danger')
        finally:
            if db.is_connected():
                cursor.close()
                db.close()
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'first_name' not in session:
        flash('You must be logged in to access the Dashboard.', 'danger')
        return redirect(url_for('login'))
    
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("SELECT first_name, middle_name, last_name, contact_number, email, address FROM adet_user WHERE first_name = %s", (session['first_name'],))
        user_details = cursor.fetchone()
    except Error as e:
        flash(f'Error occurred: {e}', 'danger')
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
    
    return render_template('dashboard.html', user_details=user_details)

@app.route('/logout')
def logout():
    session.pop('first_name', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
