from flask import Flask, render_template, request, redirect, url_for, session
import sqlstuff
app = Flask(__name__)
app.config['SECRET_KEY'] = "ghwguiasghui0"
sqlstuff.config()


@app.route("/")
def homePage():
    return render_template("index.html")

@app.route("/login-signup", methods=["POST", "GET"])
def login_signup():
    if request.method == "POST":
        if "login" in request.form:
            username=request.form['username']
            password = request.form['password']
            session['username'] = username
            session['password'] = password
            return redirect(url_for("account", username=username))
        else :
            username = request.form['username']
            password = request.form['password']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            companyname = request.form['companyname']
            sqlstuff.signupInsert('users', username, password, firstname, lastname, email, companyname)
            session["username"] = username
            session["password"] = password
            return redirect(url_for("account", username = username))
    else:
        if 'username' in session and 'password' in session:
            username = session['username']
            return redirect(url_for("account", username=username))
        else:
            return render_template("login-signup.html")

@app.route("/forgot-password", methods=["POST", "GET"])
def forgotpassword():
    if request.method == "GET":
        return render_template("forgot_password.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login_signup'))

@app.route("/account/<username>")
def account(username):
    if 'username' in session and 'password' in session:
        username = str(username)
        password = str(session['password'])
        return "<p>" + username + "</p><p>" + password + "</p>"
    else:
        return redirect(url_for('login_signup'))
    
@app.route('/account')
def accredirect():
    try:
        return redirect(url_for('account', username = session['username']))
    except:
        return redirect(url_for('login_signup'))


if __name__ == "__main__":
    app.run(Debug=True)