def user_schema(user:dict) -> dict:
    return {
        "id":str(user["_id"]),
        "name":user["name"],
        "lastname":user["lastname"],
        "username":user["username"],
        "email":user["email"],
        "birthdate":user["birthdate"],
        "password":user["password"]
        }
    
def users_schema(users) -> list:
    return [user_schema(user) for user in users] 