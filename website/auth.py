from flask import Blueprint , render_template , request , redirect , url_for , jsonify
from .models import User , Note
from werkzeug.security import generate_password_hash , check_password_hash
from . import db
from flask_login import login_user , login_required , logout_user , current_user
from email.message import EmailMessage
import ssl
import smtplib
import random
import json

from dotenv import load_dotenv
import os

scores = {} ; sum = 0 ; max = -1000 ; code = random.randint(100000 , 999999)


auth = Blueprint('auth' , __name__)



#login


@auth.route('/login' ,  methods = ["POST" , "GET"])
def login():

    global sum , max , scores

    if request.method == 'POST':
        
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()

        if user:
            if check_password_hash( user.password, password ):
                login_user(user , remember=True)

                return redirect('/home')

    return render_template("login.html")



#logout


@auth.route('/logout' )
def logout():
    logout_user()
    return redirect('/')



#sign_up

@auth.route('/sign_up' , methods = ["POST" , "GET"])

def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')


        #email sending

        load_dotenv()

        PASSWORD = os.getenv("EMAIL_PASS")

        email_sender = 'vzlatev7@gmail.com'
        email_password = PASSWORD
        email_receiver = email

        subject = "Verification code"

        global code

        body = f"""
        to prossed enter this verification code in our app : {code} 
        """ 

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context =  ssl.create_default_context()
        #end of email sending


        user = User.query.filter_by(email = email).first()

        if user:
            print('account already exists')

        else:
            new_user = User(email = email , first_name = username , password = generate_password_hash ( password , method = 'sha256' ) )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user , remember=True)
            with smtplib.SMTP_SSL('smtp.gmail.com' , 465 , context=context) as smtp :
                smtp.login(email_sender , email_password)
                smtp.sendmail(email_sender , email_receiver , em.as_string())

            return redirect('/2fa')
 
    return render_template("signup.html")



#2fa


@auth.route('/2fa' , methods = ["POST" , "GET"])
@login_required

def email():
    if request.method == 'POST':
        global code
        mycode = request.form.get('code')
        if mycode == str(code):
            return redirect('/home')
    return render_template("email.html")





#quizapp


@auth.route('/game' , methods = ["POST" , "GET"])

def game():
    return render_template("game.html")



  #savescore

@auth.route('/savescore', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    points = note['noteId']
    print(points)
    new_note = Note(data = points , user_id = current_user.id)
    db.session.add(new_note)
    db.session.commit()
    
    return jsonify({})

#end of quizz app



# profile page

@auth.route('/profile' , methods = ["POST" , "GET"] )

def profile():

    global scores
    sum = 0  ; max = -1000

    if request.method == 'GET':

        user = current_user

        for note in user.notes:
            if note in user.notes:
                if int(note.data) > max:
                    max = int(note.data)
                    ok = 0 

                    if ok == 0:
                        sum = max * 10
                    else : sum = 0 

    return render_template('profile.html' , user = user , sum = sum)




#leaderboard


headings = ['Name' , 'Points']

@auth.route('/leaderboard' , methods = ["POST" , "GET"] )

def leaderboard():

    global scores
    sum = 0 ; max = -1000

    if request.method == 'GET':

        user = current_user

        for note in user.notes:
            if note in user.notes:
                if int(note.data) > max:
                    max = int(note.data)
                    ok = 0 

                    if ok == 0:
                        sum = max * 10
                    else : sum = 0 

        scores[user.first_name] = str(sum)

        sorted_scores = sorted( scores.items(), key=lambda x:x[1], reverse=True )

        converted_dict = dict(sorted_scores)

        for i in range(len(converted_dict)):
            if i > 5:
                converted_dict.popitem()

    return render_template('leaderboard.html' , user = user , headings=headings , converted_dict = converted_dict)
