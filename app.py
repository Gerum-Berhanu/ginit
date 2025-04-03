from flask import Flask, render_template, request
import json
from solver import resolve

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve", methods = ["POST"])
def solve():
    equation = request.form.get("equation")
    solution, message = resolve(equation)
    return json.dumps({"solution": solution, "message": message})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)