from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from Backend.routers import tareas, users

app = FastAPI()
app.mount("/static", StaticFiles(directory="Frontend/static"), name="static")
# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://gestor-de-tareas-r39h.onrender.com"],  # ⚠️ en producción, mejor usar ["https://miweb.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(tareas.router)
app.include_router(users.router)

@app.get("/", status_code=200)
async def get():
    return FileResponse(os.path.join("Frontend","templates", "index.html"))

@app.get("/login", status_code=200)
async def get():
    return FileResponse(os.path.join("Frontend","templates", "login.html"))
@app.get("/register", status_code=200)
async def get():
    return FileResponse(os.path.join("Frontend","templates", "register.html"))
@app.get("/taskify", status_code=200)
async def get():
    return FileResponse(os.path.join("Frontend","templates", "tasks_main.html"))
@app.get("/create", status_code=200)
async def get():
    return FileResponse(os.path.join("Frontend","templates", "create_task.html"))
@app.get("/me/{id}", status_code=200)
async def get():
    return FileResponse(os.path.join("Frontend","templates", "view_task.html"))

