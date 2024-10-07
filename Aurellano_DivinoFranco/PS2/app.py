from flask import Flask, render_template, request, jsonify
import json
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    info = request.form.to_dict()
    
    data = {
    "firstName": info['f_name'], 
    "middleName": info['m_name'], 
    "lastName": info['l_name'], 
    "contactNumber": info['c_number'], 
    "emailAddress":info['email'], 
    "address": info['address'], 
}

    # Save data to JSON file
    with open('data.json', 'a') as f:
        json.dump(data, f)
        f.write('\n')  # Add a newline for better readability

    return jsonify({'message': 'Information saved successfully!'})

if __name__ == "__main__":
    app.run(debug=True)