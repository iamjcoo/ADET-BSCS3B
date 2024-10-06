from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        return render_template('result.html', name=name)
    return render_template('cagorong.html')

if __name__ == '__main__':
    app.run(debug=True)