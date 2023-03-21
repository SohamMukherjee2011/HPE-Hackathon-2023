from flask import Flask, render_template, request, redirect, url_for
import sqlstuff
app = Flask(__name__)
sqlstuff.config()
@app.route("/")
def homePage():
    return render_template("index.html")

@app.route("/login-signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        if "login" in request.form:
            name=request.form['username']
            password = request.form['password']
            return redirect(url_for("account", username=name, password=password))
        else :
            return redirect(url_for("homePage"))
    else:
         return render_template("login-signup.html")

@app.route("/account/<username><password>")
def account(username, password):
    username = str(username)
    password = str(password)
    return "<p>" + username + "</p><p>" + password + "</p>"

@app.route("/forgot-password", methods=["POST", "GET"])
def forgotpassword():
    if request.method == "GET":
        return render_template("forgot_password.html")

if __name__ == "__main__":
    app.run(Debug=True)