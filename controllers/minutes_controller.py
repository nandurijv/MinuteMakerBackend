from app import connect,mail
from flask import make_response,request
from flask_mail import Message
from models.user_model import User
from bson.json_util import dumps, loads
from bson import ObjectId
from pydantic import ValidationError
from os import environ
import bcrypt
import jwt
import json

class minutes_controller():
    def getall(self):
        
        return make_response({"success":"true","message":"retrieved all the messages"},200)