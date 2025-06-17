from pydantic import BaseModel
from models.users import User

class Task(BaseModel):
    id:str | None=None
    title:str
    subtitle:str
    description:str| None=None
    priority:int | None=None
    created_at:str | None=None
    expired_at:str | int | None=None
    modify_at:str | None=None
    created_by:str | None=None
    status:str | None="En progreso"
    
    