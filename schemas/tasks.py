from models.tasks import Task

def task_schema(task:dict) -> dict:
    return {
        "id":str(task["_id"]),
        "title":task["title"],
        "subtitle":(task["subtitle"]),
        "description":(task["description"] or None),
        "priority":   (task["priority"]or 0) ,
        "created_at": (task["created_at"]or None),
        "expired_at": (task["expired_at"]or None),
        "modify_at":  (task["modify_at"]or None),
        "created_by": (task["created_by"] or None),
        "status": (task["status"]) or None
        }
    
def tasks_schema(tasks) -> list:
    try:
        return [Task(**task_schema(task)) for task in tasks] 
    except Exception as e:
        return {"error inesperado en el modelado": f"{e.add_note("modelado de usuario fallido")}"}
        