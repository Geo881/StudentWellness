
#!/usr/bin/python

import sys
import json
sys.path.insert(1,'python')
sys.path.append("/var/www/html/studentwellnessflask/studentwellnessflask/python")
import crud2 as crud
from flask import Flask, render_template, request, flash ,redirect, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

#a route where we will deplay a page via HTML template

app = Flask(__name__)
mysql = MySQL(app)
app.config.from_pyfile('config.cfg')
app.secret_key = ("shhhh don't speak too loud")
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'

app.config['MYSQL_USER'] = 'swadmin'
app.config['MYSQL_PASSWORD'] = 'StudentWellness'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'studentwellness'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'



@login_manager.user_loader
def load_user(userId):
    return crud.User.getById(int(userId))



@app.route('/Register', methods=['GET', 'POST'])
def createUser():
    if request.method == 'POST':
        email = request.form['email']
        new_user = crud.createUser()
        if new_user.userExist(new_user.email,new_user.userName):
            flash("The user name or email is already in use!")
            return render_template("RegisterFRM2.html")
        new_user.create()
        token = s.dumps(email, salt='email-confirm')

        msg = Message('Confirm Student Wellness Registration', sender='ccsustudentwellnes@gmail.com', recipients=[email])
        link = url_for('confirm_email', token=token, _external=True)
        msg.body = 'Your link is {}'.format(link)
        mail.send(msg)

        return redirect(url_for('signIn'))
    return render_template("RegisterFRM2.html")

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600000)
        user =crud.User.getByEmail(email)
        user.confirmUser()
    except SignatureExpired:
        return '<h1>The link is expired!</h1>'
    return redirect(url_for('signIn'))





@app.route('/ForgetPass', methods=['GET', 'POST'])
def forgetPassword():
    if request.method == 'POST':
        email = request.form['email']
        if not crud.User.emailExist(email):
            flash("Email does not exist")
            return render_template("ResetPassT.html")
        password = crud.User.forgetPassword(email)
        msg = Message('Temporary Student Wellness Password', sender='geovanni881@gmail.com', recipients=[email])
        msg.body = 'Your temporary password is {}'.format(password)
        mail.send(msg)
        return redirect(url_for('signIn'))
    return render_template("ResetPassT.html")

@app.route('/', methods=['GET', 'POST'])
def signIn():
    if request.method == 'POST':
        userName = request.form['Username']
        inPassword = request.form['psw']
        data = crud.retreiveUserData()
        if not crud.User.userNameExist(userName):
            flash("Invalid user name")
        else:
            user = crud.User.getByUserName(userName)
            if user.validate(inPassword):
                login_user(user)
                return redirect(url_for('doWheel'))
            else:
                flash("Invalid password or Unconfirmed email")
    return render_template("index.html")



@app.route('/logOut', methods=['GET', 'POST'])
@login_required
def signOut():
    logout_user()
    return redirect(url_for('signIn'))

@app.route('/AdminSetting', methods=['GET', 'POST'])
@login_required
def adminSetting():
    if request.method == 'GET':
        return render_template("AdminSettingsPage.html", UsernameDisplay = current_user.userName, EmailDisplay = current_user.email)
    return render_template("AdminSettingsPage.html")

@app.route('/AdminRegistration', methods=['GET', 'POST'])
@login_required
def AdminRegistration():
    if request.method == 'POST':
        email = request.form['email']
        new_user = crud.createUser()
        if new_user.userExist(new_user.email, new_user.userName):
            flash("The username or email is already in use!")
            return render_template("AdminRegistration.html")
        new_user.createAdmin()
        token = s.dumps(email, salt='email-confirm')

        msg = Message('Confirm Student Wellness Registration',recipients[email], sender='ccsustudentwellness@gmail.com')
        link = url_for('confirm_email', token=token, _external=True)
        msg.body = 'Your link is {}'.format(link)
        mail.send(msg)

        return redirect(url_for('AdminSettings'))
    return render_template("AdminRegistration.html")

@login_required
@app.route('/ChangeWheel', methods=['GET', 'POST'])
def changeWheel():
    global setTemplate
    if request.method == 'GET':
        resourceList = crud.getWheelResources()
        return render_template("ChangeWheel.html", SocialResources=resourceList[0], PhysicalResources=resourceList[1], IntellectualResources=resourceList[2], FinancialResources=resourceList[3],\
               SpiritualResources=resourceList[4], EmotionalResources=resourceList[5], EnvironmentalResources=resourceList[6], OccupationalResources=resourceList[7], SocialLinks=resourceList[8],\
               PhysicalLinks=resourceList[9], IntellectualLinks=resourceList[10], FinancialLinks=resourceList[11], SpiritualLinks=resourceList[12], EmotionalLinks=resourceList[13],\
               EnvironmentalLinks=resourceList[14], OccupationalLinks=resourceList[15])
    else:
       testList = []
       testList.append(request.form.get('SocialResources'))
       testList.append(request.form.get('PhysicalResources'))
       testList.append(request.form.get('IntellectualResources'))
       testList.append(request.form.get('FinancialResources'))
       testList.append(request.form.get('SpiritualResources'))
       testList.append(request.form.get('EmotionalResources'))
       testList.append(request.form.get('EnvironmentalResources'))
       testList.append(request.form.get('OccupationalResources'))

       linksList = []

       linksList.append(request.form.get('SocialLinks'))
       linksList.append(request.form.get('PhysicalLinks'))
       linksList.append(request.form.get('IntellectualLinks'))
       linksList.append(request.form.get('FinancialLinks'))
       linksList.append(request.form.get('SpiritualLinks'))
       linksList.append(request.form.get('EmotionalLinks'))
       linksList.append(request.form.get('EnvironmentalLinks'))
       linksList.append(request.form.get('OccupationalLinks'))

       crud.changeWheel(testList,linksList)
       return redirect(url_for('adminSetting'))

@app.route('/Wheel', methods=['GET', 'POST'])
@login_required
def doWheel():
    if request.method == 'POST':
        currentResponses = request.form['sure']
        crud.pushResponses (currentResponses, current_user.userName)
        return redirect(url_for('doWheel'))
    else:
        currentUser = current_user.userName
        prevResponses = [None,None,None,None,None,None,None,None]
        getPrevs = crud.getPrevResponses(currentUser)
        for ele in getPrevs:
            prevResponses[0] = ele["social"]
            prevResponses[1] = ele["physical"]
            prevResponses[2] = ele["intellectual"]
            prevResponses[3] = ele["financial"]
            prevResponses[4] = ele["spiritual"]
            prevResponses[5] = ele["emotional"]
            prevResponses[6] = ele["environmental"]
            prevResponses[7] = ele["occupational"]

        #get resources
        resources = crud.getResources()
        links = crud.getLinks()
        return render_template("wheel.html", username = currentUser, responses = prevResponses, values = resources, links = links)

@app.route('/RegSettings', methods=['GET', 'POST'])
@login_required
def regSettings():
        print("Current status:" + str(current_user.isAdmin(current_user.userName)))
        if request.method == 'GET':
            if current_user.isAdmin(current_user.userName) == True:
                return redirect(url_for('adminSetting'))
        return render_template("RegSettingsPage.html", UsernameDisplay=current_user.userName, EmailDisplay = current_user.email)



@app.route('/Report', methods=['GET', 'POST'])
@login_required
def report():
    if request.method == 'GET':
        wellSessCnt = [crud.wellnessSessionCount()]
        values = crud.genReportDta()
        onOffCampus = crud.campusSituation()
        print(values)
        return render_template("report.html",g1Data = values[0],
                g2Data = values[1], g3Data = values[2], g4Data=values[3],
                g5Data = values[4], g6Data = values[5], g7Data = values[6],
                g8Data = values[7], g9Data = values[8], g10Data = onOffCampus,
                total = values[9],g11Data = wellSessCnt)
    if request.method == 'POST':
        if request.form["onOffCampus"] == "offCampus":
            wellSessCnt = [crud.wellnessSessionCount()]
            values = crud.genReportDtaOffCmp()
            onOffCampus = crud.campusSituation()
            flash("Showing Off-Campus Data")
            return render_template("report.html",g1Data = values[0],
            g2Data = values[1], g3Data = values[2], g4Data=values[3],
            g5Data = values[4], g6Data = values[5], g7Data = values[6],
            g8Data = values[7], g9Data = values[8], g10Data = onOffCampus,
            total = values[9],g11Data = wellSessCnt)
        elif request.form["onOffCampus"] == "onCampus":
            wellSessCnt = [crud.wellnessSessionCount()]
            values = crud.genReportDtaOnCmp()
            onOffCampus = crud.campusSituation()
            flash("Showing On-Campus Data")
            return render_template("report.html",g1Data = values[0],
            g2Data = values[1], g3Data = values[2], g4Data=values[3],
            g5Data = values[4], g6Data = values[5], g7Data = values[6],
            g8Data = values[7], g9Data = values[8], g10Data = onOffCampus,
            total = values[9],g11Data = wellSessCnt)
        elif request.form["onOffCampus"] == "aggregate":
            wellSessCnt = [crud.wellnessSessionCount()]
            values = crud.genReportDta()
            onOffCampus = crud.campusSituation()
            flash("Showing Aggregate Data")
            return render_template("report.html",g1Data = values[0],
            g2Data = values[1], g3Data = values[2], g4Data=values[3],
            g5Data = values[4], g6Data = values[5], g7Data = values[6],
            g8Data = values[7], g9Data = values[8], g10Data = onOffCampus,
            total = values[9],g11Data = wellSessCnt)

        else:
            if current_user.is_admin == 1:
                if current_user.validate(request.form['psw']):
                    if request.form['psw-repeat'] == request.form['psw']:
                        #crud.deleteUsers()
                        crud.deleteWellnessSess()
                        flash("Reset Successful")
                        return redirect(url_for('report'))
                    else:
                        flash("Passwords did that match")
                        return redirect(url_for('report'))
                else:
                    flash("Incorrect Password")
                    return redirect(url_for('report'))
            else:
                flash("ONLY AN ADMIN CAN DO THIS")
                return redirect(url_for('report'))





@app.route('/ChangePass', methods=['GET', 'POST'])
@login_required
def changePassword():
    print("Entered In")
    if request.method == 'POST':
        print("Entered Post")
        currentPass = request.form['currentPassword']
        newPass = request.form['newPassword']
        newPassConfirm = request.form['newPasswordConfirm']
        print("beyonnn")
        if newPass == newPassConfirm:
            #if  generate_password_hash(currentPass, method='sha256') == current_user.passWord:
            if current_user.validate(currentPass):
                current_user.changePassword(newPass)
                return redirect(url_for('forgetPassword'))
            else:
                flash("Password incorrect")
                return render_template("ChangePassword.html")
        else:
            flash("New passwords do not match")
            render_template("ChangePassword.html")
    return render_template("ChangePassword.html")

@app.route('/about',methods=['GET','POST'])
def about():
	return render_template("about.html")

#running the application
if __name__ == "__main__":
	app.run(debug=true)
