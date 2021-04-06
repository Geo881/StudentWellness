
from flask import Flask, render_template, request, flash ,redirect, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

import random
import string
import datetime
import json

app = Flask(__name__)
mysql = MySQL(app)
app.config.from_pyfile('config.cfg')
app.secret_key = ("shhhh don't speak too loud")
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/SignIn'



class User(UserMixin):
    def __init__(self,email=None,userName=None,passWord=None,livingSituation=None,is_admin=None):
        self.id = None
        self.email = email
        self.userName = userName
        self.passWord = passWord
        self.livingSituation = livingSituation
        self.confirmed = None
        self.is_admin = is_admin

    def create(self):
        cur = mysql.connection.cursor()
        #hashedPassword = generate_password_hash(self.passWord, method='sha256')
        cur.execute("INSERT INTO user (email,user_name,password,living_situation,\
                confirmation,is_admin)VALUES ('{0}', '{1}', '{2}', '{3}',0,0)"\
                .format(self.email,self.userName,self.passWord,self.livingSituation))
        mysql.connection.commit()
        cur.close()

    def confirmUser(self):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE user SET confirmation ='{0}' WHERE email = '{1}'".format(1,self.email))
        mysql.connection.commit()
        cur.close()

    def isAdmin(self,userName):
        cur = mysql.connection.cursor()
        #cur.execute("select is_admin from user where user_name = '{0}'").format(userName)
        cur.execute("select is_admin from user where user_name = '{0}'".format(userName))
        data = cur.fetchall()
        val = int(data[0]["is_admin"])
        if val == 1:
            return True
        else:
            return False

    @classmethod
    def getByEmail(self,email):
        cur = mysql.connection.cursor()
        cur.execute("select email, user_name, password, living_situation,\
                id, is_admin from user where email = '{0}'".format(email))
        data = cur.fetchall()
        u = User()
        if len(data) !=0:
            u.id,u.email,u.userName,u.passWord,u.livingSituation,u.is_admin = data[0]["id"],data[0]["email"]\
                ,data[0]["user_name"],data[0]["password"],data[0]["living_situation"],data[0]["is_admin"]

            #u.id,u.email,u.userName,u.passWord,u.livingSituation = data[0][4],data[0][0]\
            #        ,data[0][1],data[0][2],data[0][3]
        cur.close()
        return u

    @classmethod
    def emailExist(self,email):
        cur = mysql.connection.cursor()
        cur.execute("select email from user")
        data = cur.fetchall()
        cur.close()
        val = False
        emails = [ele["email"] for ele in data ]
        #emails = [ele[0] for ele in data ]

        if email in emails:
            val = True
        return val


    @classmethod
    def userExist(self,email,userName):
        cur = mysql.connection.cursor()
        cur.execute("select email, user_name from user")
        data = cur.fetchall()
        cur.close()
        val = False
        userNames = [ele["user_name"] for ele in data ]
        emails = [ele["email"] for ele in data ]
        #userNames = [ele[1] for ele in data ]
        #emails = [ele[0] for ele in data ]

        if email in emails or userName in userNames:
            val = True
        return val

    @classmethod
    def userNameExist(self,userName):
        cur = mysql.connection.cursor()
        cur.execute("select user_name from user")
        data = cur.fetchall()
        cur.close()
        val = False
        userNames = [ele["user_name"] for ele in data ]
        #userNames = [ele[0] for ele in data ]
        if userName in userNames:
            val = True
        return val

    def changePassword(self, newPassword):
        cur = mysql.connection.cursor()
        hashedPassword = generate_password_hash(newPassword, method = 'sha256')
        cur.execute("UPDATE user SET password = '{0}' WHERE user_name = '{1}' ".format(hashedPassword, self.userName))
        mysql.connection.commit()
        cur.close()



    @classmethod
    def resetPassword(self,email,newPassword):
        cur = mysql.connection.cursor()
        hashedPassword = generate_password_hash(newPassword, method='sha256')
        cur.execute("UPDATE user SET password = '{0}' WHERE email ='{1}' ".format(hashedPassword,email))
        mysql.connection.commit()
        cur.close()


    def validate(self,password):
        if check_password_hash(self.passWord,password) and int(self.confirmed) == 1:
            return True
        else:
            return False



    
    @classmethod
    def forgetPassword(self,email):
        cur = mysql.connection.cursor()
        size = 9 
        chars=string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for _ in range(size))
        hashedPassword = generate_password_hash(password, method='sha256')
        cur.execute("UPDATE user SET password = '{0}' WHERE email ='{1}' ".format(hashedPassword,email))
        mysql.connection.commit()
        cur.close()
        return password





    @classmethod
    def getByUserName(self,userName):
        cur = mysql.connection.cursor()
        cur.execute("select email, user_name, password, living_situation,\
                id,confirmation,is_admin from user where user_name = '{0}'".format(userName))
        data = cur.fetchall()
        u = User()
        if len(data) !=0:
            u.id,u.email,u.userName,u.passWord,u.livingSituation,u.confirmed,u.is_admin = data[0]["id"],data[0]["email"]\
                ,data[0]["user_name"],data[0]["password"],data[0]["living_situation"],data[0]["confirmation"]\
                ,data[0]["is_admin"]

            #u.id,u.email,u.userName,u.passWord,u.livingSituation,u.confirmed = data[0][4],data[0][0]\
            #        ,data[0][1],data[0][2],data[0][3],data[0][5]
        cur.close()
        return u


    @classmethod
    def getById(self,userId):
        cur = mysql.connection.cursor()
        cur.execute("select email, user_name, password, living_situation,\
                 id,confirmation,is_admin from user where id = '{0}'".format(userId))
        data = cur.fetchall()
        print(data)
        u = User()
        if len(data) !=0:
            u.id,u.email,u.userName,u.passWord,u.livingSituation,u.confirmed,u.is_admin = data[0]["id"],data[0]["email"]\
                ,data[0]["user_name"],data[0]["password"],data[0]["living_situation"],data[0]["confirmation"]\
                ,data[0]["is_admin"]

            #u.id,u.email,u.userName,u.passWord,u.livingSituation,u.confirmed = data[0][4],data[0][0]\
            #        ,data[0][1],data[0][2],data[0][3],data[0][5]
        cur.close()
        return u
        
def createUser():
        email = request.form['email']
        userName = request.form['Username']
        passWord = request.form['psw']
        hashedPassword = generate_password_hash(passWord, method='sha256')
        livingSituation = request.form['living']
        new_user = User(email,userName,hashedPassword,livingSituation)
        return new_user

def retreiveUserData():
        userName = request.form['Username']
        InPassword = request.form['psw']
        cur = mysql.connection.cursor()
        cur.execute("select user_name,password from user where user_name = '{0}'".format(userName))
        data = cur.fetchall()
        cur.close()
        return data

def checkUser(userName,inPassword):
        cur = mysql.connection.cursor()
        cur.execute("select password from user where user_name = '{0}'".format(userName))
        data = cur.fetchall()
        #passWord = data[0]['password']
        passWord = data[0][0]
        print("This is the value for the password for db " +passWord )
        user = User.getByUserName(userName)
        cur.close()
        print("This is the value for confirmation "+str(user.confirmed))
        print("This the value of passWord " + passWord)
        print("This the value of inPassword " + inPassword)
        print("Truth value " + str(check_password_hash(passWord,inPassword)))
        if check_password_hash(passWord,inPassword) and int(user.confirmed) == 1:
            #login_user(user)
            print("trueeeeeeeeeeeeeeeeeeeeeeeee")
            return True
        else:
            print("falseeeeeeeeeeeeeeeeeeeee")
            return False



def pw_gen(size = 9, chars=string.ascii_letters + string.digits + string.punctuation):
	return ''.join(random.choice(chars) for _ in range(size))



def changeWheel(resources,links):

    cur = mysql.connection.cursor()
    
    cur.execute("""SET sql_mode = ''""")

    cur.execute("""TRUNCATE resources2""")
    cur.execute("""TRUNCATE resource_links2""")

    try:

        splitSocial = resources[0].splitlines()
        for ele in splitSocial:
          if ele and (not ele.isspace()):
            try:
                ele = ele.replace("{'wellness_type': 'social', 'response': '", "")
                ele = ele.replace("'}", "")
                finalSocial = ele.split("', 'message': '")
                wellness_type = 'social'
                response = finalSocial[0]
                message = finalSocial[1]
                cur.execute("""INSERT INTO resources2 (wellness_type, response, message) VALUES ('{0}' , '{1}' , '{2}')""".format(wellness_type, response, message))
            except:
                print("Exception")

        splitPhysical = resources[1].splitlines()
        for ele in splitPhysical:
          if ele and (not ele.isspace()):
            try:
                ele = ele.replace("{'wellness_type': 'physical', 'response': '", "")
                ele = ele.replace("'}", "")
                finalPhysical = ele.split("', 'message': '")
                wellness_type = 'physical'
                response = finalPhysical[0]
                message = finalPhysical[1]
                cur.execute("""INSERT INTO resources2 (wellness_type, response, message) VALUES ('{0}' , '{1}' , '{2}')""".format(wellness_type, response, message))
            except:
                print("Exception")

        splitIntellectual = resources[2].splitlines()
        for ele in splitIntellectual:
          if ele and (not ele.isspace()):
            try:
                ele = ele.replace("{'wellness_type': 'intellectual', 'response': '", "")
                ele = ele.replace("'}", "")
                finalIntellectual = ele.split("', 'message': '")
                wellness_type = 'intellectual'
                response = finalIntellectual[0]
                message = finalIntellectual[1]
                cur.execute("""INSERT INTO resources2 (wellness_type, response, message) VALUES ('{0}' , '{1}' , '{2}')""".format(wellness_type, response, message))
            except:
                print("Exception")

        splitFinancial = resources[3].splitlines()
        for ele in splitFinancial:
          if ele and (not ele.isspace()):
            try:
                ele = ele.replace("{'wellness_type': 'financial', 'response': '", "")
                ele = ele.replace("'}", "")
                final = ele.split("', 'message': '")
                wellness_type = 'financial'
                response = final[0]
                message = final[1]
                cur.execute("""INSERT INTO resources2 (wellness_type, response, message) VALUES ('{0}' , '{1}' , '{2}')""".format(wellness_type, response, message))
            except:
                print("Exception")

        splitSpiritual = resources[4].splitlines()
        for ele in splitSpiritual:
          if ele and (not ele.isspace()):
            try:
                ele = ele.replace("{'wellness_type': 'spiritual', 'response': '", "")
                ele = ele.replace("'}", "")
                final = ele.split("', 'message': '")
                wellness_type = 'spiritual'
                response = final[0]
                message = final[1]
                cur.execute("""INSERT INTO resources2 (wellness_type, response, message) VALUES ('{0}' , '{1}' , '{2}')""".format(wellness_type, response, message))
            except:
                print("Exception")

        splitEmotional = resources[5].splitlines()
        for ele in splitEmotional:
          if ele and (not ele.isspace()):
            try:
                ele = ele.replace("{'wellness_type': 'emotional', 'response': '", "")
                ele = ele.replace("'}", "")
                final = ele.split("', 'message': '")
                wellness_type = 'emotional'
                response = final[0]
                message = final[1]
                cur.execute("""INSERT INTO resources2 (wellness_type, response, message) VALUES ('{0}' , '{1}' , '{2}')""".format(wellness_type, response, message))
            except:
                print("Exception")

        splitEnvironmental = resources[6].splitlines()
        for ele in splitEnvironmental:
          if ele and (not ele.isspace()):
            try:
                ele = ele.replace("{'wellness_type': 'environmental', 'response': '", "")
                ele = ele.replace("'}", "")
                final = ele.split("', 'message': '")
                wellness_type = 'environmental'
                response = final[0]
                message = final[1]
                cur.execute("""INSERT INTO resources2 (wellness_type, response, message) VALUES ('{0}' , '{1}' , '{2}')""".format(wellness_type, response, message))
            except:
                print("Exception")

        splitOccupational = resources[7].splitlines()
        for ele in splitOccupational:
          if ele and (not ele.isspace()):
            try:
                ele = ele.replace("{'wellness_type': 'occupational', 'response': '", "")
                ele = ele.replace("'}", "")
                final = ele.split("', 'message': '")
                wellness_type = 'occupational'
                response = final[0]
                message = final[1]
                cur.execute("""INSERT INTO resources2 (wellness_type, response, message) VALUES ('{0}' , '{1}' , '{2}')""".format(wellness_type, response, message))
            except:
                print("Exception")

        socialLink = links[0].splitlines()
        for ele in socialLink:
          if ele and (not ele.isspace()):
            try:
                ele = ele.replace("{'resource_type': 'social', 'label': '", "")
                ele = ele.replace("'}", "")
                final = ele.split("', 'resource_link': '")
                resource_type = 'social'
                label = final[0]
                resource_link = final[1]
                cur.execute("""INSERT INTO resource_links2 (resource_type, label, resource_link) VALUES ('{0}' , '{1}' , '{2}')""".format(resource_type, label, resource_link))
            except:
                print("Exception")

        physicalLink = links[1].splitlines()
        for ele in physicalLink:
          if ele and (not ele.isspace()):
            try:
                ele = ele.replace("{'resource_type': 'physical', 'label': '", "")
                ele = ele.replace("'}", "")
                final = ele.split("', 'resource_link': '")
                resource_type = 'physical'
                label = final[0]
                resource_link = final[1]
                cur.execute("""INSERT INTO resource_links2 (resource_type, label, resource_link) VALUES ('{0}' , '{1}' , '{2}')""".format(resource_type, label, resource_link))
            except:
                print("Exception")

        intellectualLink = links[2].splitlines()
        for ele in intellectualLink:
          if ele and (not ele.isspace()):
            try:
                ele = ele.replace("{'resource_type': 'intellectual', 'label': '", "")
                ele = ele.replace("'}", "")
                final = ele.split("', 'resource_link': '")
                resource_type = 'intellectual'
                label = final[0]
                resource_link = final[1]
                cur.execute("""INSERT INTO resource_links2 (resource_type, label, resource_link) VALUES ('{0}' , '{1}' , '{2}')""".format(resource_type, label, resource_link))
            except:
                print("Exception")

        financialLink = links[3].splitlines()
        for ele in financialLink:
          if ele and (not ele.isspace()):
            try:
                ele = ele.replace("{'resource_type': 'financial', 'label': '", "")
                ele = ele.replace("'}", "")
                final = ele.split("', 'resource_link': '")
                resource_type = 'financial'
                label = final[0]
                resource_link = final[1]
                cur.execute("""INSERT INTO resource_links2 (resource_type, label, resource_link) VALUES ('{0}' , '{1}' , '{2}')""".format(resource_type, label, resource_link))
            except:
                print("Exception")

        spiritualLink = links[4].splitlines()
        for ele in spiritualLink:
          if ele and (not ele.isspace()):
            try:
                ele = ele.replace("{'resource_type': 'spiritual', 'label': '", "")
                ele = ele.replace("'}", "")
                final = ele.split("', 'resource_link': '")
                resource_type = 'spiritual'
                label = final[0]
                resource_link = final[1]
                cur.execute("""INSERT INTO resource_links2 (resource_type, label, resource_link) VALUES ('{0}' , '{1}' , '{2}')""".format(resource_type, label, resource_link))
            except:
                print("Exception")

        emotionalLink = links[5].splitlines()
        for ele in emotionalLink:
          if ele and (not ele.isspace()):
            try:
                ele = ele.replace("{'resource_type': 'emotional', 'label': '", "")
                ele = ele.replace("'}", "")
                final = ele.split("', 'resource_link': '")
                resource_type = 'emotional'
                label = final[0]
                resource_link = final[1]
                cur.execute("""INSERT INTO resource_links2 (resource_type, label, resource_link) VALUES ('{0}' , '{1}' , '{2}')""".format(resource_type, label, resource_link))
            except:
                print("Exception")

        environmentalLink = links[6].splitlines()
        for ele in environmentalLink:
          if ele and (not ele.isspace()):
            try:
                ele = ele.replace("{'resource_type': 'environmental', 'label': '", "")
                ele = ele.replace("'}", "")
                final = ele.split("', 'resource_link': '")
                resource_type = 'environmental'
                label = final[0]
                resource_link = final[1]
                cur.execute("""INSERT INTO resource_links2 (resource_type, label, resource_link) VALUES ('{0}' , '{1}' , '{2}')""".format(resource_type, label, resource_link))
            except:
                print("Exception")

        occupationalLink = links[7].splitlines()
        for ele in occupationalLink:
          if ele and (not ele.isspace()):
            try:
                ele = ele.replace("{'resource_type': 'occupational', 'label': '", "")
                ele = ele.replace("'}", "")
                final = ele.split("', 'resource_link': '")
                resource_type = 'occupational'
                label = final[0]
                resource_link = final[1]
                cur.execute("""INSERT INTO resource_links2 (resource_type, label, resource_link) VALUES ('{0}' , '{1}' , '{2}')""".format(resource_type, label, resource_link))
            except:
                print("Exception")
            
    except:
        print("An exception occured in changeWheel")
    mysql.connection.commit()
    cur.close()


def getWheelResources():


    SocialResources = ""
    SocialLinks = ""
    PhysicalResources = ""
    PhysicalLinks = ""
    IntellectualResources = ""
    IntellectualLinks = ""
    FinancialResources = ""
    FinancialLinks = ""
    SpiritualResources = ""
    SpiritualLinks = ""
    EmotionalResources = ""
    EmotionalLinks = ""
    EnvironmentalResources = ""
    EnvironmentalLinks = ""
    OccupationalResources = ""
    OccupationalLinks = ""

    cur = mysql.connection.cursor()

    cur.execute("SELECT * from resources2 where wellness_type = 'social'")

    for ele in cur.fetchall():
        SocialResources += str(ele) + "\r"

    cur.execute("SELECT * from resource_links2 where resource_type = 'social'")

    for ele in cur.fetchall():
       SocialLinks += str(ele) + "\r"

    cur.execute("SELECT * from resources2 where wellness_type = 'physical'")
    for ele in cur.fetchall():
       PhysicalResources += str(ele) + "\r"

    cur.execute("SELECT * from resource_links2 where resource_type = 'physical'")

    for ele in cur.fetchall():
       PhysicalLinks += str(ele) + "\r"

    cur.execute("SELECT * from resources2 where wellness_type = 'intellectual'")
    for ele in cur.fetchall():
      IntellectualResources += str(ele) + "\r"

    cur.execute("SELECT * from resource_links2 where resource_type = 'intellectual'")
    for ele in cur.fetchall():
      IntellectualLinks += str(ele) + "\r"

    cur.execute("SELECT * from resources2 where wellness_type = 'financial'")
    for ele in cur.fetchall():
       FinancialResources += str(ele) + "\r"

    cur.execute("SELECT * from resource_links2 where resource_type = 'financial'")
    for ele in cur.fetchall():
       FinancialLinks += str(ele) + "\r"

    cur.execute("SELECT * from resources2 where wellness_type = 'spiritual'")
    for ele in cur.fetchall():
       SpiritualResources += str(ele) + "\r"

    cur.execute("SELECT * from resource_links2 where resource_type = 'spiritual'")
    for ele in cur.fetchall():
      SpiritualLinks += str(ele) + "\r"

    cur.execute("SELECT * from resources2 where wellness_type = 'emotional'")
    for ele in cur.fetchall():
       EmotionalResources += str(ele) + "\r"

    cur.execute("SELECT * from resource_links2 where resource_type = 'emotional'")
    for ele in cur.fetchall():
       EmotionalLinks += str(ele) + "\r"

    cur.execute("SELECT * from resources2 where wellness_type = 'environmental'")
    for ele in cur.fetchall():
       EnvironmentalResources += str(ele) + "\r"

    cur.execute("SELECT * from resource_links2 where resource_type = 'environmental'")
    for ele in cur.fetchall():
       EnvironmentalLinks += str(ele) + "\r"

    cur.execute("SELECT * from resources2 where wellness_type = 'occupational'")
    for ele in cur.fetchall():
       OccupationalResources += str(ele) + "\r"

    cur.execute("SELECT * from resource_links2 where resource_type = 'occupational'")
    for ele in cur.fetchall():
       OccupationalLinks += str(ele) + "\r"

    cur.close()

    return list([SocialResources,PhysicalResources,IntellectualResources, FinancialResources,SpiritualResources,EmotionalResources, EnvironmentalResources,OccupationalResources, SocialLinks, PhysicalLinks, IntellectualLinks, FinancialLinks, SpiritualLinks, EmotionalLinks, EnvironmentalLinks, OccupationalLinks])

def getPrevResponses(user):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT social,environmental,spiritual,emotional,occupational,physical,financial,intellectual,dates  from wellness_session ws where ws.dates = (select max(ws2.dates) from wellness_session ws2 where ws2.user_name = '{0}')""".format(user))
    responses = cur.fetchall()
    return responses

def getResources():
    cur = mysql.connection.cursor()
    cur.execute("SELECT *  from resources2")
    resources = cur.fetchall()
    return resources

def getLinks():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from resource_links2")
    links = cur.fetchall()
    return links

def pushResponses(currResponses, user):
    cur = mysql.connection.cursor()
    cur.execute("""SET sql_mode = ''""")
    social = int(currResponses[0])
    physical = int(currResponses[2])
    intellectual =  int(currResponses[4])
    financial = int(currResponses[6])
    spiritual =  int(currResponses[8])
    emotional = int(currResponses[10])
    environmental =  int(currResponses[12])
    occupational = int(currResponses[14])
    currentuser = user
    currentdate = datetime.datetime.now();
    currentdate = currentdate.strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""INSERT INTO wellness_session (user_name, social, physical, intellectual, financial, spiritual, emotional, environmental, occupational, dates) VALUES ('{0}' , '{1}' , '{2}' , '{3}' , '{4}' , '{5}' , '{6}' , '{7}' , '{8}' , '{9}' )""".format(currentuser, social, physical, intellectual, financial, spiritual, emotional, environmental, occupational, currentdate))
    mysql.connection.commit()
    cur.close



def campusSituation():
    values = []
    cur = mysql.connection.cursor()
    cur.execute("select count(*) as amount from user where living_situation=1")
    data = cur.fetchall()[0]["amount"]
    values.append(data)
    cur.execute("select count(*) as amount from user where living_situation=0")
    data = cur.fetchall()[0]["amount"]
    values.append(data)
    cur.close()
    return values

def deleteUsers():
    cur = mysql.connection.cursor()
    cur.execute("delete from user where is_admin = 0")
    mysql.connection.commit()
    cur.close()




def deleteWellnessSess():
    cur = mysql.connection.cursor()
    cur.execute("delete from wellness_session")
    mysql.connection.commit()
    cur.close()

def wellnessSessionCount():
    cur = mysql.connection.cursor()
    cur.execute("SELECT count(*) as amount from wellness_session ws where ws.dates =\
            (select max(ws2.dates) from wellness_session ws2 where \
            ws2.user_name=ws.user_name);")
    data = cur.fetchall()[0]["amount"]
    cur.close()
    return data



def genReportDta():
    values = []
    cur = mysql.connection.cursor()
    cur.execute("select count(user_name) as amount from user")
    data = cur.fetchall()[0]["amount"]
    values.append([data])
    cur.execute("SELECT * from wellness_session ws where ws.dates =\
            (select max(ws2.dates) from wellness_session ws2 where \
            ws2.user_name=ws.user_name);")
    data = cur.fetchall()
    wellnessValues = [[0,0,0,0,0,0,0,0] ,[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    wellnessLabels= ["social","environmental","spiritual","emotional"\
            ,"occupational","physical","financial","intellectual"]
    for ele in data:
        for i in range(8):
            wellnessValues[ele[wellnessLabels[i]]-1][i]+=1

    wellnessTotal = [0,0,0,0,0,0,0,0]

    sessionCount = wellnessValues[0][0]+ wellnessValues[1][0]+ wellnessValues[2][0]

    values.append([wellnessValues[0][0],wellnessValues[1][0],wellnessValues[2][0]])
    values.append([wellnessValues[0][1],wellnessValues[1][1],wellnessValues[2][1]])
    values.append([wellnessValues[0][2],wellnessValues[1][2],wellnessValues[2][2]])
    values.append([wellnessValues[0][3],wellnessValues[1][3],wellnessValues[2][3]])
    values.append([wellnessValues[0][4],wellnessValues[1][4],wellnessValues[2][4]])
    values.append([wellnessValues[0][5],wellnessValues[1][5],wellnessValues[2][5]])
    values.append([wellnessValues[0][6],wellnessValues[1][6],wellnessValues[2][6]])
    values.append([wellnessValues[0][7],wellnessValues[1][7],wellnessValues[2][7]])


    sessionCount = wellnessValues[0][0]+ wellnessValues[1][0]+ wellnessValues[2][0]
    values.append(sessionCount)
    cur.close()
    return values






def genReportDtaOnCmp():
    values = []
    cur = mysql.connection.cursor()
    cur.execute("select count(user_name) as amount from user")
    data = cur.fetchall()[0]["amount"]
    values.append([data])
    cur.execute("select social, environmental, spiritual, emotional,occupational,\
            physical,financial, intellectual from (SELECT * from wellness_session\
            ws where ws.dates = (select max(ws2.dates) from wellness_session ws2\
            where ws2.user_name=ws.user_name)) t1 where exists (select * from user\
            where living_situation = 1 and user.user_name = t1.user_name);"  )
    data = cur.fetchall()
    wellnessValues = [[0,0,0,0,0,0,0,0] ,[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    wellnessLabels= ["social","environmental","spiritual","emotional"\
            ,"occupational","physical","financial","intellectual"]
    for ele in data:
        for i in range(8):
            wellnessValues[ele[wellnessLabels[i]]-1][i]+=1

    wellnessTotal = [0,0,0,0,0,0,0,0]

    sessionCount = wellnessValues[0][0]+ wellnessValues[1][0]+ wellnessValues[2][0]

    values.append([wellnessValues[0][0],wellnessValues[1][0],wellnessValues[2][0]])
    values.append([wellnessValues[0][1],wellnessValues[1][1],wellnessValues[2][1]])
    values.append([wellnessValues[0][2],wellnessValues[1][2],wellnessValues[2][2]])
    values.append([wellnessValues[0][3],wellnessValues[1][3],wellnessValues[2][3]])
    values.append([wellnessValues[0][4],wellnessValues[1][4],wellnessValues[2][4]])
    values.append([wellnessValues[0][5],wellnessValues[1][5],wellnessValues[2][5]])
    values.append([wellnessValues[0][6],wellnessValues[1][6],wellnessValues[2][6]])
    values.append([wellnessValues[0][7],wellnessValues[1][7],wellnessValues[2][7]])


    sessionCount = wellnessValues[0][0]+ wellnessValues[1][0]+ wellnessValues[2][0]
    values.append(sessionCount)
    cur.close()
    return values



def genReportDtaOffCmp():
    values = []
    cur = mysql.connection.cursor()
    cur.execute("select count(user_name) as amount from user")
    data = cur.fetchall()[0]["amount"]
    values.append([data])
    cur.execute("select social, environmental, spiritual, emotional,occupational,\
            physical,financial, intellectual from (SELECT * from wellness_session\
            ws where ws.dates = (select max(ws2.dates) from wellness_session ws2\
            where ws2.user_name=ws.user_name)) t1 where exists (select * from user\
            where living_situation = 0 and user.user_name = t1.user_name);"  )
    data = cur.fetchall()
    wellnessValues = [[0,0,0,0,0,0,0,0] ,[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    wellnessLabels= ["social","environmental","spiritual","emotional"\
            ,"occupational","physical","financial","intellectual"]
    for ele in data:
        for i in range(8):
            wellnessValues[ele[wellnessLabels[i]]-1][i]+=1

    wellnessTotal = [0,0,0,0,0,0,0,0]

    sessionCount = wellnessValues[0][0]+ wellnessValues[1][0]+ wellnessValues[2][0]

    values.append([wellnessValues[0][0],wellnessValues[1][0],wellnessValues[2][0]])
    values.append([wellnessValues[0][1],wellnessValues[1][1],wellnessValues[2][1]])
    values.append([wellnessValues[0][2],wellnessValues[1][2],wellnessValues[2][2]])
    values.append([wellnessValues[0][3],wellnessValues[1][3],wellnessValues[2][3]])
    values.append([wellnessValues[0][4],wellnessValues[1][4],wellnessValues[2][4]])
    values.append([wellnessValues[0][5],wellnessValues[1][5],wellnessValues[2][5]])
    values.append([wellnessValues[0][6],wellnessValues[1][6],wellnessValues[2][6]])
    values.append([wellnessValues[0][7],wellnessValues[1][7],wellnessValues[2][7]])


    sessionCount = wellnessValues[0][0]+ wellnessValues[1][0]+ wellnessValues[2][0]
    values.append(sessionCount)
    cur.close()
    return values
