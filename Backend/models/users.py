from pydantic import BaseModel

class User(BaseModel):
    id:str | None=None
    name:str
    lastname:str
    username:str
    email:str
    birthdate:str
    password:str
    disabled:bool|None=False
    
class LoginUser(BaseModel):
    username:str|None=None
    email:str|None=None
    password:str