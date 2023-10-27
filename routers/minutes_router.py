from middlewares.auth_controller import auth_model
from app import app
from controllers.minutes_controller import minutes_controller
from flask import request

obj = minutes_controller()
authenticator=auth_model()

@app.route("/minutes/getall")
@authenticator.token_auth
def getallminutes():
    return obj.getall()

@app.route("/minutes/getminutesbyid", methods=["POST"])
@authenticator.token_auth
def getminutesbyid():
    # id = request.json["id"]
    return obj.getminutesbyid("653b5a5cdd8dd0ccb4e8e06e")

@app.route("/minutes/generate", methods=["POST"])
@authenticator.token_auth
def generateminutes():
    return obj.generateminutes(request)

@app.route("/minutes/save", methods=["POST"])
@authenticator.token_auth
def saveminutes():
    return obj.saveminutes(request)