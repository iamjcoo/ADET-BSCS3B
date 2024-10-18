from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            return "Name is required", 400
        return redirect(url_for('greet', name=name))
    return render_template('index.html')

@app.route('/hello/<name>')
def greet(name):
    return render_template('greeting.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
