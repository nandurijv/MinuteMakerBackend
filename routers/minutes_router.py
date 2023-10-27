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


@app.route("/minutes/add", methods=["POST"])
@authenticator.token_auth
def addminutes():
    return obj.addminutes(request)