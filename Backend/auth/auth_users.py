from Backend.models.users import User
from Backend.schemas.users import user_schema, users_schema
from Backend.db.client import db
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
import os,jwt, re
from bson import ObjectId
from passlib.context import CryptContext
from dotenv import load_dotenv


load_dotenv("env/.env")
SECRET=os.getenv("SECRET_KEY")
ALGORITHM="HS256"

pwd_context=CryptContext(schemes="bcrypt", deprecated="auto")

oauth2 = OAuth2PasswordBearer(tokenUrl="login")



#Esto verifica el estado del token y si el ingresado existe o no.
def current_user(token:str = Depends(oauth2)): 
    try:
        access_token:dict = jwt.decode(token,SECRET, algorithms=[ALGORITHM])
        username = access_token.get("sub")
        if username == None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail=f"Credenciales de autenticacion invalidas",
                            headers={"www-Authenticate":"Bearer"})
        return SearchUser.by_username(username)
    except :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail=f"Token inválido o expirado: ",
                            headers={"www-Authenticate":"Bearer"})
    
    
def auth_user(user:User = Depends(current_user)): #?Verifica el estado del usuario (Enabled/Disabled)
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario deshabilitado")
    return user
        
def hash_password(password: str) -> str:
    return str(pwd_context.hash(password))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def encode(access_token):
    return jwt.encode(access_token, SECRET, ALGORITHM)

def decode (token):
    return jwt.decode(token,SECRET, algorithms=[ALGORITHM])
class SearchUser:
    def get_all():
        return users_schema(db.main.users.find())
    
    def by_id(id:str):
        try:
            return User(**user_schema(db.main.users.find_one({"_id":ObjectId(id)})))
        except:
            return None
    def by_username(username:str):
        try:
            return User(**user_schema(db.main.users.find_one({"username":username})))
        except:
            return None
    def by_email(email:str):
        try:
            return User(**user_schema(db.main.users.find_one({"email":email})))
        except:
            return None
        
class Auth:
    def email(email:str):
        match_email=re.search(r"[\w.%_áéíúóñ+-]+@[a-zA-Z]+\.[a-zA-Z]{0,2}\.?[a-zA-Z]{0,2}", email)
        if match_email == None:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "El email ingresado no es válido. Ingrese un email del estilo: 'tu_email@empresa.dominio' para continuar")
        if db.main.users.find_one({"email":email}) != None:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "El email ingresado ya está en uso")
    
    def username(username:str):
        match_user=re.search(r"^[a-zA-Záéíóú][\w_a-zA-Záéíóú]{3,20}$", username)
        if match_user == None:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 
                            "El nombre de usuario ingresado no es válido.\nRequisitos:\nDebe contener entre 8 y 20 carácteres.\nSolo puede contener caracteres alfanumericos y '_'\nEl primer caracter debe ser alfabético (a-z, A-Z)")
        if db.main.users.find_one({"username":username}) != None:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "El usuario ingresado ya está en uso")
    
    def birthdate(birthdate:str):
        match_birthdate=re.search(r"\b\d{2}/\d{2}/\d{4}\b",birthdate)
        if match_birthdate == None:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 
                            "La fecha ingresada no es válida. Asegúrese que cumpla con el formato 'dd/mm/yyyy'")
    
    def password(password:str):
        match_password=re.search(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@#$%&?¿]).{8,20}$",password)
        if match_password == None:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 
                            "La contraseña ingresada no es válida.\nRequisitos:\nAl menos un caracter especial (@#$%&?¿)\nEntre 8 y 20 caracteres\nAl menos una letra\nAl menos un número")              