from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    name = None
    if request.method == "POST":
        name = request.form.get("username")  
    if name:
        greeting = f"Hello World! {name}, welcome to CCCS 106 - Applications Development and Emerging Technologies"
    else:
        greeting = "Hello, World!"
    return render_template("main.html", greeting=greeting)

if __name__ == "__main__":
    app.run(debug=True)
