from app import app
from controllers.user_controller import user_controller
from flask import request

obj = user_controller()

@app.route("/user/getall")
def getall():
    return obj.getall()

@app.route("/user/getbyid/<id>")
def getbyid(id):
    return obj.getbyid(id)

@app.route("/user/signup",methods=["POST"])
def signup():
    return obj.signup(request.json)

@app.route("/user/login",methods=["POST"])
def login():
    return obj.login(request.json)

@app.route("/user/verify/<token>")
def verify(token):
    return obj.verify(token)

@app.route("/user/resendmail",methods=["POST"])
def sendmail():
    return obj.send_mail(request.json)
