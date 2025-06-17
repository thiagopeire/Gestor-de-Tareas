from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import tareas, users


app = FastAPI()
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # ⚠️ en producción, mejor usar ["https://miweb.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(tareas.router)
app.include_router(users.router)
#Guardar en otra base de datos la relacion de usuarios y tareas por medio de un token de acceso 

#C:\Library\bin  #Ruta de base de datos