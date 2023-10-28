from flask import Flask
from database.connection import connection
from flask_mail import Mail
from flask_cors import CORS, cross_origin
import os
# initialise flask application
app= Flask(__name__)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = os.getenv("SENDER_MAIL"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
))
mail = Mail(app)
cors = CORS(app)

# connect to database
connect = connection().connect()

#start page
@app.route("/")
@cross_origin()
def welcome():
    return "MinutesMaker: Backend is Up and Running"

# import other controllers
from routers import *