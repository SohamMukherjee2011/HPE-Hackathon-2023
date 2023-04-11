from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlstuff
import encryption
app = Flask(__name__)
app.config['SECRET_KEY'] = "ghwguiasghui0"
sqlstuff.config()


@app.route("/")
def homePage():
    if 'email' in session:
        return render_template("home.html",login=True)
    else:
        return render_template("home.html",login=False)

@app.route("/login-signup", methods=["POST", "GET"])
def login_signup():
    if request.method == "POST":
        if "login" in request.form:
            email=request.form['email']
            password = request.form['password']
            table = sqlstuff.showall('userlist')
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
            table = sqlstuff.showall('userlist')
            for x in table:
                if email == x[0]:
                    flash("Email ID already in use", "info")
                    return redirect(url_for("login_signup"))
                    break
            else:
                    passwordEnc = encryption.encrypt(password)
                    sqlstuff.signupInsert('userlist',email, passwordEnc[1], firstname, lastname, companyname, passwordEnc[0])
                    session["email"] = email
                    session["password"] = password
                    session["firstname"] = firstname
                    session["lastname"] = lastname
                    session["companyname"] = companyname
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
        accList = sqlstuff.showField('userlist', 'email', email)
        for x in accList:
            global firstname, lastname, companyname
            firstname = x[2]
            lastname = x[3]
            companyname = x[4]
        sqlstuff.deleteSingleRow('userlist', 'email', email)
        sqlstuff.signupInsert('userlist', email, passwordEnc[1], firstname, lastname, companyname, passwordEnc[0])
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
    session.pop('firstname', None)
    session.pop('lastname', None)
    session.pop('companyname', None)
    return redirect(url_for('login_signup'))

@app.route("/account/<email>", methods=["GET", "POST"])
def account(email):
    if request.method == "POST":
        newFname = request.form['firstname']
        newLname = request.form['lastname']
        newCompname = request.form['companyname']
        if newFname != "":
            sqlstuff.update('userlist', 'firstname', newFname, 'email', email)
            session['firstname'] = newFname
        if newLname != "":
            sqlstuff.update('userlist', 'lastname', newLname, 'email', email)
            session['lastname'] = newLname
        if newCompname != "":        
            sqlstuff.update('userlist', 'companyname', newCompname, 'email', email)
            session['companyname'] = newCompname
        flash("Changes saved successfully", 'info')
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

@app.route('/blogs/stop-getting-hacked')
def stop():
    return render_template('stop getting hacked.html')

@app.route('/blogs/cyber-security-101')
def security():
    return render_template('cybersecurity.html')
# quizzes part begins from here

@app.route('/quizdashboard')
def quizdashboard():
    if 'email' in session and 'password' in session:
        email = session['email']
        rowlist = sqlstuff.showField('quizresult', 'email', email)
        quizlist = []
        i = 0
        for valuelist in rowlist:
            i = i + 1
            print(valuelist[4])
            quizlist.append((valuelist[1], valuelist[2], bool(valuelist[4]), i, valuelist[5]))
        return(render_template('quizdashboard.html', quizlist=quizlist))
    else:
        return redirect(url_for('login_signup'))

@app.route('/quizzes/<quizname>', methods = ["GET", "POST"])
def quiz(quizname):
    quizdata = sqlstuff.showField('quizzes', 'link','/quizzes/' + quizname)
    if request.method == "GET":
            if quizdata == []:
                return redirect(url_for('login_signup'))
            else: 
                return render_template('quiz_template.html', quizdata = quizdata)
    else:
        result = []
        score = 0
        for y in quizdata:
            #form-data collection
            global quizname1
            quizname1 = y[0]
            useroption = request.form[y[1]]
            i = 0
            optionstemp = str(y[4])
            optionstemp = list(optionstemp.split(","))
            options = []
            optiondict = {}
            for x in optionstemp:
                x = x.replace("'", '')
                x = x.replace('[', '')
                x = x.replace(']', '')
                options.append(x.strip())
            optiondict['A'] = options[0]
            optiondict['B'] = options[1]
            optiondict['C'] = options[2]
            optiondict['D'] = options[3]
            if optiondict[useroption] == y[2]:
                score = score + 1
                print(score)
                result.append(1)
                print(result)
            else:
                result.append(0)
        score = int(score*25)
        sqlstuff.quizresultinsert('quizresult', session['email'], y[0], score, str(result), True, '/quizzes/' +  quizname)
        return render_template('quiz_result.html', score=score)
            


if __name__ == "__main__":
    app.run(Debug=True) 