from flask import Flask, render_template, request, redirect, url_for, session, flash
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
            email=request.form['email']
            password = request.form['password']
            table = sqlstuff.showall('users')
            i = 0
            for x in table:
                print(x[0])
                if email == x[0]:
                    if password == x[1]:
                        session['email'] = email
                        session['password'] = password
                        return redirect(url_for("account", email = email))
                        break
                    else:
                        flash('Wrong Password', 'info')
                        return redirect(url_for('login_signup'))
                else:
                    if i >= len(table):
                        flash('Invalid Email ID', 'info')
                        return redirect(url_for("login_signup"))
                i += 1
        else :
            email = request.form['email']
            password = request.form['password']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            companyname = request.form['companyname']
            table = sqlstuff.showall('users')
            for x in table:
                if email == x[0]:
                    flash("Email ID already in use", "info")
                    return redirect(url_for("login_signup"))
                    break
            else:
                    sqlstuff.signupInsert('users',email, password, firstname, lastname, companyname)
                    session["email"] = email
                    session["password"] = password
                    return redirect(url_for("account", email = email))
    else:
        if 'email' in session and 'password' in session:
            email = session['email']
            return redirect(url_for("account", email = email))
        else:
            return render_template("login-signup.html")

@app.route("/forgot-password", methods=["POST", "GET"])
def forgotpassword():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        sqlstuff.update('users', ['password'], [str(password)], 'email', str(email))
        session["email"] = email
        session["password"] = password
        flash("password changed", "info")
        return redirect(url_for("account", email = email))
    else:
        return render_template("forgot_password.html")

@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('password', None)
    return redirect(url_for('login_signup'))

@app.route("/account/<email>")
def account(email):
    if 'email' in session and 'password' in session:
        email = str(email)
        password = str(session['password'])
        return render_template("account_temp.html", email = email, password = password)
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