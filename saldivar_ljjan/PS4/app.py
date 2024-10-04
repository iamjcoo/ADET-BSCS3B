from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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
        password = request.form.get('password')  
        hashed_password = hash_password(password) 

        # Save to MySQL database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            insert_query = '''
                INSERT INTO adet_user (first_name, middle_name, last_name, birthdate, email, address, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (first_name, middle_name, last_name, birthdate, email, address, hashed_password))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('success')) 
        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template('register.html')

@app.route('/success')
def success():
    return redirect(url_for('login'))  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check the credentials
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM adet_user WHERE email = %s', (username,))
            user = cursor.fetchone()  
            cursor.close()  
            conn.close()  

            # Verify password
            if user:
                hashed_password = user[7]  
                if hashlib.sha256(password.encode()).hexdigest() == hashed_password:
                    session['user_id'] = user[0]  
                    session['first_name'] = user[1]  
                    session['middle_name'] = user[2]  
                    session['last_name'] = user[3]
                    session['email'] = user[4]
                    session['address'] = user[5]
                    return redirect(url_for('dashboard'))
                else:
                    # Redirect to registration page if login fails
                    flash("Invalid credentials. Please register if you don't have an account.")
                    return redirect(url_for('register'))
            else:
                # Redirect to registration page if no user found
                flash("Invalid credentials. Please register if you don't have an account.")
                return redirect(url_for('register'))

        except mysql.connector.Error as err:
            return f"Database error: {err}"

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_details = {
        'first_name': session['first_name'],
        'middle_name': session.get('middle_name', ''),
        'last_name': session['last_name'],
        'email': session['email'],
        'address': session['address']
    }
    return render_template('dashboard.html', user=user_details)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('first_name', None)
    session.pop('middle_name', None)
    session.pop('last_name', None)
    session.pop('email', None)
    session.pop('address', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
