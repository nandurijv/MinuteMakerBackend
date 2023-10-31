from middlewares.auth_controller import auth_model
from app import app, cross_origin
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
    id = request.json["id"]
    return obj.getminutesbyid(id)

@app.route("/minutes/generate/audio", methods=["POST"])
@authenticator.token_auth
def generateminutesbyaudio():
    return obj.generateminutesbyaudio(request)

@app.route("/minutes/generate/transcript", methods=["POST"])
@authenticator.token_auth
def generateminutesbytranscript():
    return obj.generateminutesbytranscript(request)

@app.route("/minutes/save", methods=["POST"])
@authenticator.token_auth
def saveminutes():
    return obj.saveminutes(request)

@app.route("/minutes/download", methods=["POST"])
@authenticator.token_auth
def downloadminutes():
    return obj.save_as_docx(request.json)

@app.route("/minutes/delete", methods=["DELETE"])
@authenticator.token_auth
def deleteminutes():
    id = request.json["id"]
    return obj.deleteminute(id)

@app.route("/minutes/update", methods=["PUT"])
@cross_origin()
@authenticator.token_auth
def updateminutes():
    return obj.updateminute(request.json)