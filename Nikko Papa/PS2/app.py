from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = "secret" 
# File path for storing user data
USER_DATA_FILE = 'registered.json'

# Helper function to save data to JSON file
def save_data(data, filename=USER_DATA_FILE):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Helper function to load data from JSON file
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
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Validation
        if not name or not email or not password:
            flash("All fields are required!", "danger")
            return redirect(url_for('register'))
        
        # Load existing users
        users = load_data()

        # Check if email already exists
        if any(user['email'] == email for user in users):
            flash("Email already registered!", "danger")
            return redirect(url_for('register'))
        
        # Add new user
        new_user = {
            'name': name,
            'email': email,
            'password': password
        }
        users.append(new_user)

        # Save the updated users list to the JSON file
        save_data(users)

        flash("Successfully Registered!", "success")
        return redirect(url_for('register'))

    return render_template('registration.html')

if __name__ == '__main__':
    app.run(debug=True)
