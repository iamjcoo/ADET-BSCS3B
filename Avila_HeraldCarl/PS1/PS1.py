from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('PS1.html')

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form['name']
    return f'<h1>Hello World!</h> <h1>{name}, welcome to CCCS 106 - Applications Development and Emerging Technologies</h1>'

if __name__ == '__main__':
    app.run(debug=True)