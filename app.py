from flask import Flask
from database.connection import connection

# initialise flask application
app= Flask(__name__)

# connect to database
connect = connection().connect()

#start page
@app.route("/")
def welcome():
    return "MinutesMaker: Backend is Up and Running"

@app.route("/home")
def home():
    return "This is homepage"

# import other controllers
from controller import *