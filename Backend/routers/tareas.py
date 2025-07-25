from Backend.models.tasks import Task
from Backend.auth.auth_users import current_user, decode
from fastapi import APIRouter, HTTPException, status, Depends
from Backend.db.client import db
from Backend.models.users import User
from Backend.schemas.tasks import task_schema, tasks_schema
from bson import ObjectId
from datetime import datetime, timedelta
from Backend.schemas.users import user_schema

router = APIRouter(prefix="/tasks", tags=["Tareas"])


@router.get("/me")  # Llamar a todas las tareas
async def task_get_one(user=Depends(current_user)):
    user_id = user.id
    return SearchTask.get_all(user_id)


@router.get("/me/view/{id}")
async def task_get_one(id, _=Depends(current_user)):
    return SearchTask.by_id(id)


@router.post("/create", status_code=201,)
async def task_create(task: Task, user: User = Depends(current_user)):
    task_dict = dict(task)
    task_dict["created_by"] = user.id
    del task_dict["id"]
    try:
        expiracion = Tarea.expiration(task_dict['expired_at'])
        task_dict.update({"created_at": str(Time.now()), "expired_at": expiracion,
                         "priority": 0 if task_dict["priority"] == None else task_dict["priority"]})
        db.main.tasks.insert_one(task_dict)
        return Task(**task_schema(task_dict))
    except Exception:
        raise TaskError.GenericError()


@router.put("/update", status_code=status.HTTP_202_ACCEPTED)
async def task_update(task_updated: Task, _: User = Depends(current_user)):

    id = task_updated.id
    dict_task: dict = Tarea.VerifyExpiredAt(dict(task_updated))
    del dict_task["id"]
    try:
        dict_task["created_at"] = SearchTask.by_id(id)["created_at"]
        dict_task["created_by"] = SearchTask.by_id(id)["created_by"]
        dict_task["modify_at"] = Time.now()
        end_task = db.main.tasks.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": dict_task}, return_document=True)
        return Task(**task_schema(end_task))
    except Exception as e:
        raise TaskError.GenericError(status.HTTP_404_NOT_FOUND, detail=e)


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def task_delete(id: str, _: User = Depends(current_user)):
    try:
        db.main.tasks.find_one_and_delete({"_id": ObjectId(id)})
    except:
        raise TaskError.GenericError()


class SearchTask:
    def get_all(id):
        try:
            return tasks_schema(db.main.tasks.find({"created_by": id}))
        except Exception:
            raise TaskError.GenericError(status.HTTP_404_NOT_FOUND)

    def by_id(id: str):
        try:
            return task_schema(db.main.tasks.find_one({"_id": ObjectId(id)}))
        except Exception:
            raise TaskError.GenericError(status.HTTP_404_NOT_FOUND)

    def by_creator_id(creator_id: str):
        try:
            return task_schema(db.main.tasks.find_one({"created_by": creator_id}))
        except Exception:
            raise TaskError.GenericError(status.HTTP_404_NOT_FOUND)


class SearchUser:
    def by_username(username: str):
        try:
            return user_schema(db.main.users.find_one({"username": username}))
        except Exception:
            raise TaskError.GenericError(status.HTTP_404_NOT_FOUND)


class Time:
    def now():
        return str(datetime.now().strftime("%y/%m/%d - %H:%M:%S"))


class Tarea:  # Clase que maneja las funciones de las tareas
    def expiration(expiration: int):
        try:
            return (str((timedelta(minutes=float(expiration))+datetime.now()).strftime("%H:%M:%S")))
        except:
            return False

    # Verifica si hay algun valor, si lo hay lo actualiza a datetime y sino lo deja asi
    def VerifyExpiredAt(dict_task: dict):
        # Si existe un valor en expired_at lo convierte a una fecha y hora y lo devuelve en el diccionario
        if dict_task["expired_at"] != "No especificado" or dict_task["expired_at"] != False:
            expiracion = Tarea.expiration(dict_task['expired_at'])
            dict_task["expired_at"] = expiracion
        return dict_task


class TaskError(HTTPException):  # Defino una clase propia para los errores genericos
    def __init__(self):
        super().__init__()

    def GenericError(statuscode: status = status.HTTP_400_BAD_REQUEST, detail=None):
        raise HTTPException(status_code=statuscode,
                            detail=f"Ocurrió un error {detail}")


class Token:
    def user(token):
        print(token)
        token = decode(bytes(token))
        print(token)
        return token.sub
