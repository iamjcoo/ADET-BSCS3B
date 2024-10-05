from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = "secret"

USER_DATA_FILE = 'C:\\Users\\cagor\\OneDrive\\Documents\\ADET-BSCS3B\\Cagorong_Jane\\PS2\\registered.json'


def save_data(data, filename=USER_DATA_FILE):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def load_data(filename=USER_DATA_FILE):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        address = request.form['address']
    
        if not first_name or not last_name or not email or not contact_number or not address:
            flash("All fields are required!", "danger")
            return redirect(url_for('register'))
        
        users = load_data()

        if any(user['email'] == email for user in users):
            flash("Email already registered!", "danger")
            return redirect(url_for('register'))
        
        new_user = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'contact_number': contact_number,
            'email': email,
            'address': address,
        }
        users.append(new_user)

        save_data(users)

        flash("Successfully Registered!", "success")
        return redirect(url_for('register'))

    return render_template('registration.html')

if __name__ == '__main__':
    app.run(debug=True)
