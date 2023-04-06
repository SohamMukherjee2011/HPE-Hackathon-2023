from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlstuff
import encryption
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
                if email == x[0]:
                    passwordDec = encryption.decrypt(x[5], x[1])
                    if password == str(passwordDec):
                        session['email'] = email
                        session['password'] = password
                        session['firstname'] = x[2]
                        session['lastname'] = x[3]
                        session['companyname'] = x[4]
                        return redirect(url_for("account", email = email))
                        break
                    else:
                        flash('Wrong Password', 'info')
                        return redirect(url_for('login_signup'))
                else:   
                        flash('Invalid Email ID', 'info')
                        return redirect(url_for("login_signup"))
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
                    passwordEnc = encryption.encrypt(password)
                    sqlstuff.signupInsert('users',email, passwordEnc[1], firstname, lastname, companyname, passwordEnc[0])
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
        passwordEnc = encryption.encrypt(password)
        accList = sqlstuff.showField('users', 'email', email)
        for x in accList:
            global firstname, lastname, companyname
            firstname = x[2]
            lastname = x[3]
            companyname = x[4]
        sqlstuff.deleteSingleRow('users', 'email', email)
        sqlstuff.signupInsert('users', email, passwordEnc[1], firstname, lastname, companyname, passwordEnc[0])
        session["email"] = email
        session["password"] = password
        session['firstname'] = x[2]
        session['lastname'] = x[3]
        session['companyname'] = x[4]
        flash("password changed", "info")
        return redirect(url_for("account", email = email))
    else:
        return render_template("forgot_password.html")

@app.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('password', None)
    return redirect(url_for('login_signup'))

@app.route("/account/<email>", methods=["GET", "POST"])
def account(email):
    if request.method == "POST":
        newFname = request.form['firstname']
        newLname = request.form['lastname']
        newCompname = request.form['companyname']
        sqlstuff.update('users', 'firstname', newFname, 'email', email)
        sqlstuff.update('users', 'lastname', newLname, 'email', email)
        sqlstuff.update('users', 'companyname', newCompname, 'email', email)
        session['firstname'] = newFname
        session['lastname'] = newLname
        session['companyname'] = newCompname
        return redirect(url_for('account', email = email))

    else:
        if 'email' in session and 'password' in session:
            if email == session['email']:
                email = str(email)
                password = str(session['password'])
                firstname=str(session['firstname'])
                lastname=str(session['lastname'])
                companyname=str(session['companyname'])
                return render_template("account.html", email = email, password = password, 
                                       firstname=firstname, lastname=lastname, companyname=companyname)
            else:
                return redirect(url_for('login_signup'))
        else:
            return redirect(url_for('login_signup'))
    
@app.route('/account')
def accredirect():
    try:
        return redirect(url_for('account', username = session['username']))
    except:
        return redirect(url_for('login_signup'))

#blogs part begins here
@app.route('/blogs')
def blogdashboard():
    bloglist = sqlstuff.showall('bloglist')
    blogList = []
    for x in bloglist:
        for y in x:
            blogList.append(y)
    i = 0
    blogNumber = ""
    while i < len(blogList): 
        blogNumber = blogNumber + str(i)
        i = i + 3
    return render_template('bloglist.html', bloglist=blogList, blogNumber = str(blogNumber))

# quizzes part begins from here

@app.route('/quizzes')
def quizdashboard():
    if 'email' in session and 'password' in session:
        return("Quiz moment")
    else:
        return redirect(url_for('login_signup'))

if __name__ == "__main__":
    app.run(Debug=True)