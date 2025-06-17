from Backend.models.users import User
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from Backend.db.client import db 
from Backend.auth.auth_users import Autorizar,SearchUser,hash_password,verify_password,encode
from Backend.schemas.users import user_schema, users_schema
from datetime import datetime, timedelta
from urllib.parse import unquote

router=APIRouter(prefix="/users", tags=["Usuarios"])
TIMETOEXPIRE=36 #hours

@router.get("/", status_code=status.HTTP_202_ACCEPTED)
async def users_get_all():
    return users_schema(db.main.users.find())

@router.post("/register", status_code=status.HTTP_201_CREATED) #/register path
async def register_user(user:User):
    user_dict=dict(user)
    del user_dict["id"]
    password=unquote(user_dict["password"],"utf-8")
    hashed_password = hash_password(password)
    user_dict["password"]=hashed_password
    
    Autorizar.birthdate(user.birthdate)
    Autorizar.username(user.username)    
    Autorizar.email(user.email)
    Autorizar.password(user.password)    
               
    try:        
        db.main.users.insert_one(user_dict)
        return User(**user_schema(user_dict))
    except Exception as e:
        #return HTTPException(status.HTTP_400_BAD_REQUEST, detail="Ocurrio un error inesperado")
        return f"{e}"
@router.post("/login") #/login path 
async def login_user(user:OAuth2PasswordRequestForm= Depends()):
    if user.username == None: #?Verifica si se ha ingresado un usuario retorna un error esta vacio
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ingrese un nombre de usuario")
    
    user_of_db:User = SearchUser.by_username(user.username) #?Busca el usuario en base de datos ya sea con email o con usuario
    if user_of_db == None: #?Verifica si el usuario se encontro o no
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ingresado no existe")
    
    if not verify_password(user.password, user_of_db.password): #?True/False - Verifica la contraseña con la de base de datos
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="La contraseña ingresada es incorrecta")
    
    access_token=encode({
        "sub":user_of_db.username,
        "exp":int((datetime.now()+timedelta(hours=TIMETOEXPIRE)).timestamp())
    })
    
    return {"access_token":access_token}





