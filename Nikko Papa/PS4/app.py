import json
import mysql.connector
import hashlib
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin123',
    database='adet'
)

cursor = db.cursor()

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
        }
        cursor.execute(
            "INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address) VALUES (%s, %s, %s, %s, %s, %s)",
            (data['first_name'], data['middle_name'], data['last_name'], data['contact_number'], data['email'], data['address'])
        )
        db.commit()
        return redirect(url_for('home'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
