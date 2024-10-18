import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
        with open('registrations.json', 'a') as f:
            json.dump(data, f)
            f.write('\n') 
        return redirect(url_for('home'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
