from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# Path to store the JSON file
DATA_FILE = 'registrations.json'

def save_to_json(data):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r+') as file:
            file_data = json.load(file)
            file_data.append(data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
    else:
        with open(DATA_FILE, 'w') as file:
            json.dump([data], file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        contact_number = request.form.get('contact_number')
        email = request.form.get('email')
        address = request.form.get('address')

        if not (first_name and last_name and contact_number and email and address):
            return "All fields are required", 400

        # Save form data to JSON
        form_data = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'contact_number': contact_number,
            'email': email,
            'address': address
        }
        save_to_json(form_data)

        return redirect(url_for('success'))

    return render_template('index.html')

@app.route('/success')
def success():
    return "Registration successful!"

if __name__ == '__main__':
    app.run(debug=True)
