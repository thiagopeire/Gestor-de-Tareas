from pymongo import MongoClient
from fastapi import HTTPException

db=MongoClient("mongodb+srv://thiagopeire123:Thrasher616@cluster0.emhux4u.mongodb.net/", 27017)
try:
    db.admin.command("ping")
    print("✅ Conectado a MongoDB")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    raise HTTPException(
        status_code=500,
        detail=f"No se pudo conectar a MongoDB: {e}"
    )
