from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml
import MySQLdb

app = Flask(__name__)

db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_pass']
app.config['MYSQL_DB'] = db['mysql_db']

mysql =MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('PS3.html')

@app.route('/submit', methods=['POST'])
def submit_post():
    if request.method == 'POST':
        create = request.form
        fname = create['fname']
        mname = create['mname']
        lname = create['lname']
        bdate = create['bdate']
        email = create['email']
        address = create['address']
        
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO adet_avila(fname, mname, lname, bdate, email, address) VALUES(%s, %s, %s, %s, %s, %s)", (fname, mname, lname, bdate, email, address))
            mysql.connection.commit()
            return render_template('home.html', message="Information successfully recorded!")
        except MySQLdb.IntegrityError as e:
            
            if e.args[0] == 1062:
                return render_template('PS3.html', message="Email is already taken. Use other email instead.")
            else:
                return render_template('home.html', message="An error occured" + str(e))
            
        except MySQLdb.Error as e:
            return render_template('home.html' ,message="A database error occurred: " + str(e))
        finally:
            cur.close()
        
if __name__ == '__main__':
    app.run(debug=True)