from app import connect
class user_model():
    def user_signup_model(self):
        # business logic
        user = {
            "_id":1,
            "name":"nanduri",
            "email":"vishnunanduri8@gmail.com"
        }
        users = connect.users
        try:
            user_id = users.insert_one(user).inserted_id
        except:
            return {"error":"cannot insert user"}