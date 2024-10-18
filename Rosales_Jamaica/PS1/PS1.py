from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            return f"Hello! {name}, welcome to CCCS 106 - Applications Development and Emerging Technologies "
        else:
            return "Hello! Please enter your name."
    return render_template('PS1.html')

if __name__ == '__main__':
    app.run(debug=True)