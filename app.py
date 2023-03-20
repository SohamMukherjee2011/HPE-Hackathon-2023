from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def homePage():
    return render_template("index.html")

@app.route("/login-signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
     return render_template("login-signup.html")

if __name__ == "__main__":
    app.run(Debug=True)