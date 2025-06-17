from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from Backend.routers import tareas, users


app = FastAPI()
app.mount("/", StaticFiles(directory="Frontend", html=True), name="static")
app.mount("/static", StaticFiles(directory="Frontend/static"), name="static")
# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://gestor-de-tareas-r39h.onrender.com", "*"],  # ⚠️ en producción, mejor usar ["https://miweb.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(tareas.router)
app.include_router(users.router)
#Guardar en otra base de datos la relacion de usuarios y tareas por medio de un token de acceso 

#C:\Library\bin  #Ruta de base de datos

@app.get("/", status_code=200)
async def get():
    return FileResponse(os.path.join("Frontend", "index.html"))