# Late Night Coders Project for HPE Hackathon 2023
# Members: Soham Mukherjee, Shubhodeep Paul, Agniva Roy
# this is the file containing the full backend 
# refer to sqlstuff.py for sql commands and initialisation
# and to encryption.py for the code behind password encryption


# import statements
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlstuff
import encryption
app = Flask(__name__)
app.config['SECRET_KEY'] = "ghwguiasghui0"
sqlstuff.config()

# slightly responsive homepage, navbar changes according to login status
@app.route("/")
def homePage():
    if 'email' in session:
        return render_template("home.html",login=True)
    else:
        return render_template("home.html",login=False)

# pretty self explanatory, the login and signup code are here 
@app.route("/login-signup", methods=["POST", "GET"])
def login_signup():
    if request.method == "POST":
        # login code
        if "login" in request.form:
            email=request.form['email']
            password = request.form['password']
            table = sqlstuff.showall('userlist')
            for x in table:
                if email == x[0]:
                    passwordDec = encryption.decrypt(x[5], x[1])
                    # checking for correct password
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
            # if for loop is done and still there has been no redirection
            # it means email id is invalid
            else:   
                flash('Invalid Email ID', 'info')
                return redirect(url_for("login_signup"))
        # signup code
        else :
            email = request.form['email']
            password = request.form['password']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            companyname = request.form['companyname']
            table = sqlstuff.showall('userlist')
            # checks whether email id is already registered or not
            for x in table:
                if email == x[0]:
                    flash("Email ID already in use", "info")
                    return redirect(url_for("login_signup"))
                    break
            else:
                    passwordEnc = encryption.encrypt(password)
                    # account database insertion
                    sqlstuff.signupInsert('userlist',email, passwordEnc[1], firstname, lastname, companyname, passwordEnc[0])
                    # session craetion
                    session["email"] = email
                    session["password"] = password
                    session["firstname"] = firstname
                    session["lastname"] = lastname
                    session["companyname"] = companyname
                    # quizlist empty insertion for account
                    quizlist = sqlstuff.showall('quizlist')
                    for x in quizlist:
                        name = x[0]
                        link = x[1]
                        sqlstuff.quizresultinsert('quizresult', email, name, None, None, False, link)
                    return redirect(url_for("account", email = email))
    # redirects to account page if already logged in
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
        # note: password is blob type, which cannot be updated 
        # therefore account instance is deleted and inserted again
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

# account dashboard backend
@app.route("/account/<email>", methods=["GET", "POST"])
def account(email):
    # the code behind 'save changes'
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
            # if user randomly just types a link
            # e.g. https://<website>/account/abcdfjeigh
            # this will redirect to login page since the typed id doesn't exist
            else:
                return redirect(url_for('login_signup'))
        # if user not logged in, redirect to login-signup page    
        else:
            return redirect(url_for('login_signup'))

# basically redirects to account page (used for login-signup)   
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

# blogs are hard coded right now, we will add dynamic blogs using mysql 
# the tables are ready for that
# and an option for account holders to create blogs on their own
@app.route('/blogs/stop-getting-hacked')
def stop():
    return render_template('stop getting hacked.html')

@app.route('/blogs/cyber-security-101')
def security():
    return render_template('cybersecurity.html')


# quizzes part begins from here
# quizdashboard: contains all the quiz information
@app.route('/quizdashboard')
def quizdashboard():
    if 'email' in session and 'password' in session:
        email = session['email']
        rowlist = sqlstuff.showField('quizresult', 'email', email)
        quizlist = []
        i = 0
        averageScore = 0
        for valuelist in rowlist:
            i = i + 1
            if type(valuelist[2]) == 'int':
            # average score calculation part 1
                averageScore += valuelist[2]
            # list created for frontend Jinja
            quizlist.append((valuelist[1], valuelist[2], bool(valuelist[4]), i, valuelist[5]))
        # average score calculation part 2
        averageScore = int(averageScore/len(rowlist))
        return(render_template('quizdashboard.html', quizlist=quizlist, averageScore = averageScore))
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
        # calcuation of result using quiz question data from database 
        # and user data from form submission
        result = []
        score = 0
        for y in quizdata:
            global quizname1
            quizname1 = y[0]
            useroption = request.form[y[1]]
            optionstemp = str(y[4])
            # splits the string options into list
            optionstemp = list(optionstemp.split(","))
            options = []
            optiondict = {}
            # this part can be updated 
            for x in optionstemp:
                x = x.replace("'", '')
                x = x.replace('[', '')
                x = x.replace(']', '')
                options.append(x.strip())
            # doing assignment manually is easier than doing it automatically using a while loop
            # simpler, and takes up less lines of code
            optiondict['A'] = options[0]
            optiondict['B'] = options[1]
            optiondict['C'] = options[2]
            optiondict['D'] = options[3]
            if optiondict[useroption] == y[2]:
                score = score + 1
                result.append(1)
            else:
                result.append(0)
        score = int(score*25)
        quizresults = sqlstuff.showall('quizresult')
        # deletes the previous quiz result if user has already attempted the quiz 
        # or if the quiz is unattempted.
        for x in quizresults:
            if x[1] == quizname1:
                sqlstuff.deleteSingleRow('quizresult', 'quizname', quizname1)
        sqlstuff.quizresultinsert('quizresult', session['email'], y[0], score, str(result), True, '/quizzes/' +  quizname)
        # gets quiz questions data (same as in GET request part, without the average score part)
        quizdata = sqlstuff.showField('quizzes', 'link','/quizzes/' + quizname)
        return render_template('quiz_result.html', score=score, quizdata=quizdata)
            

# runs the app only if this file is running
if __name__ == "__main__":
    app.run(Debug=True) 