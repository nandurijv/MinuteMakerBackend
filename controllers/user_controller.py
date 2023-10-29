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
class user_controller():
    #get all the user
    def getall(self):
        try:
            users = connect.users.find()
            return make_response({"success":"true","message":"users retrieved successfully","data":json.loads(dumps(list(users)))},200)
        except Exception:
            return make_response({"success":"false","message":"server error"},500)
    #get by id
    def getbyid(self, id):
        try:
            users = connect.users.find({"_id":ObjectId(id)})
            return make_response({"success":"true","message":"users retrieved successfully","data":json.loads(dumps(list(users)))},200)
        except Exception:
            return make_response({"success":"false","message":"server error"},500)
    #signup control
    def signup(self, user):
        # get the collection of users
        users = connect.users
        # check if user already exists
        try:
            temp_user=user
            User(**temp_user)
        except ValidationError as e:
            return make_response({"success":"false","message":",".join([msg["msg"] for msg in e.errors()])},200)
        # if exists, return response
        check = users.find_one({"email":user["email"]})
        if check:
            return make_response({"success":"false","message":"user already exists"},200)
        #else insert the user
        else:
            # hash password
            hashed = bcrypt.hashpw(user["password"].encode('utf-8'), bcrypt.gensalt())
            user["password"]=hashed
            user["verified"]="0"
            # try inserting user
            user_id = users.insert_one(user).inserted_id
            # send mail for verification
            self.send_mail(user)

            return make_response({"success":"true","message":"user created successfully and verification mail sent!","data":str(user_id)})
    
    # login control  
    def login(self, user):
        users=connect.users
        # check if user exists
        check = users.find_one({"email":user["email"]})
        print(check)
        if check is not None:
            # if user exists, check if he is verified.
            if check["verified"]=="1":
                # now validate credentials
                if bcrypt.checkpw(user["password"].encode("utf-8"),check["password"]):
                    #create a payload
                    payload = jwt.encode({
                        "email": check["email"]
                    },environ.get("SECRET"),algorithm="HS256")
                    return make_response({"success":"true","message":"successfully logged in","data":payload},200)
                else:
                    return make_response({"success":"false","message":"password does not match"},200)
            else:
                return make_response({"success":"false","message":"user not verified"},200)
        # if user does not exist return
        else:
            return make_response({"success":"false","message":"user does not exist"},200)

    
    # verification control
    def verify(self, token):
        try:
            print(token)
            user = jwt.decode(token, environ.get("SECRET"),algorithms=["HS256"])
            check = connect.users.find_one({"email":user["email"]})
            print("hello", user)
            if check:
                # check if user already verified
                if check["verified"]=="1":
                    return make_response({"success":"true","message":"user already verified"},200)
                else:
                    # update the verified status to 1
                    connect.users.update_one({"email":user["email"]},{"$set":{"verified":"1"}})
                    return make_response({"success":"true","message":"user verified successfully"},200)
            else:
                return make_response({"success":"false","message":"user does not exist"},200)
        except Exception as e:
            return make_response({"success":"false","message":"user token invalid"},200)
    
    # send mail to user
    def send_mail(self, user):
            check = connect.users.find_one({"email":user["email"]})
            if check["verified"]=="1":
                return make_response({"success":"false","message":"user already verified"},200)
            else:
                encoded_jwt = jwt.encode({"email":user["email"]},environ.get("SECRET"),algorithm="HS256")
                msg = Message("Hello", sender=environ.get("SENDER_MAIL"),recipients=[user["email"]])
                msg.html = "<h1>Welcome to Minutes Maker!</h1> <p>Testing Phase. Verify your email address by clicking this <a href='{}' target='_blank'>link</a>.</p>".format(environ.get("BASE_URL")+"/user/verify/"+encoded_jwt)
                try:
                    mail.send(msg)
                except Exception as err:
                    print(err)
                    return {"success":False, "message":"Error Sending Mail"}
                return {"success":True, "message":"Verification Mail Sent!"}
       