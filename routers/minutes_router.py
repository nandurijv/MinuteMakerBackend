from middlewares.auth_controller import auth_model
from app import app, cross_origin
from controllers.minutes_controller import minutes_controller
from flask import request
import  requests
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

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

@app.route("/minutes/summary", methods=["POST"])
@cross_origin()
def getsummary():
    try:
        endpoint = "https://1b04-34-170-240-137.ngrok.io" # Replace with your endpoint
        usermessage = request.json["transcript"][:100]
        response_final = "write me a Summary abstract, keypoints and conclusion of the meeting thatt starts with the following" + usermessage+"..."+ "\n"+"in the following way : " + "1. Abstract" + "\n" + "2. Key Points" + "\n" + "3. Conclusion"
        payload = {
            "body": json.dumps({
                "messageResponse": response_final
            })
        }

        response = requests.post(f"{endpoint}/chatbot", json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to send POST request. HTTP Status Code: {response.status_code}")
            return {"message": f"Failed to send POST request. HTTP Status Code: {response.status_code}"}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"message": f"An error occurred: {e}"}