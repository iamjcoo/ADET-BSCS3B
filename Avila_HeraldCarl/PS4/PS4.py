from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import hashlib
import yaml
import MySQLdb

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_pass']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('log-sign-dash.html')

@app.route('/signIn')
def signIn():
    return render_template('sign-in.html')

@app.route('/signUp')
def signUp():
    return render_template('sign-up.html')

@app.route('/signIn', methods=['POST'])
def signIn_post():
    if request.method == 'POST':
        login = request.form
        email = login['email']
        password = login['password']
        
        hashed_pass_signIn = hashlib.sha256(password.encode()).hexdigest()

        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM uAccounts WHERE email = %s AND password = %s", (email, hashed_pass_signIn))

        if result > 0:
            user_account = cur.fetchone()
            cur.execute("SELECT * FROM adet_avila WHERE email = %s", (email,))
            user_details = cur.fetchone()
            session['user_details'] = {
                'first_name': user_details[1],
                'middle_name': user_details[2],
                'last_name': user_details[3],
                'contact_number': user_details[4],
                'address': user_details[5],
                'email_address': user_details[6]
            }
            return redirect(url_for('dashboard'))
        else: 
            return render_template('sign-in.html', message="Invalid Email or Password. Please try again.")

@app.route('/signUp', methods=['POST'])
def signUp_post():
    if request.method == 'POST':
        create = request.form
        fname = create['fname']
        mname = create['mname']
        lname = create['lname']
        contact_num = create['contact_num']
        address = create['address']
        email = create['email']
        password = create['confirm_password']
        
        hashed_pass_signUp = hashlib.sha256(password.encode()).hexdigest()
        
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO adet_avila(fname, mname, lname, contact_num, address, email) VALUES(%s, %s, %s, %s, %s, %s)", (fname, mname, lname, contact_num, address, email))
            cur.execute("INSERT INTO uaccounts(email, password) VALUES(%s, %s)", (email, hashed_pass_signUp))
            mysql.connection.commit()
            return render_template('log-sign-dash.html', message="Sign-up successful. Please Sign-in")
        except MySQLdb.IntegrityError as e:
            if e.args[0] == 1062:
                return render_template('sign-up.html', message="Email is already taken. Use other email instead.")
            else:
                return render_template('home.html', message="An error occurred: " + str(e))
        except MySQLdb.Error as e:
            return render_template('home.html', message="A database error occurred: " + str(e))
        finally:
            cur.close()
    else: 
        return render_template('sign-up.html')

@app.route('/dashboard')
def dashboard():
    if 'user_details' in session:
        return render_template('dashboard.html', user_details=session['user_details'])
    else:
        return redirect(url_for('signIn'))

@app.route('/logout')
def logout():
    session.pop('user_details', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)