from flask import Blueprint , render_template , request , redirect , url_for
from flask_login import login_user , login_required , logout_user , current_user
        
views = Blueprint('views' , __name__)

@views.route('/')

def home():
    return render_template("base.html")


@views.route('/home' , methods = ["POST" , "GET"])

def home2():
    if request.method == "POST":
        return render_template("article.html")
    return render_template("home.html")
