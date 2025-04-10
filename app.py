from flask import Flask, render_template, request
import json
from solver_web import resolve

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve", methods = ["POST"])
def solve():
    equation = request.form.get("equation")
    lowerBound = float(request.form.get("lowerBound") or -100)
    upperBound = float(request.form.get("upperBound") or 100)
    
    solution, message = resolve(equation, lowerBound, upperBound)
    return json.dumps({"solution": solution, "message": message})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)