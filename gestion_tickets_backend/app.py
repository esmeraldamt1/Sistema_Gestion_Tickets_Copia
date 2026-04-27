import mongoengine

def connect_to_mongo():
    """Conecta a MongoDB usando mongoengine."""
    try:
        mongoengine.connect(
            db="ticketsdb",
            host="mongodb://127.0.0.1:27017/ticketsdb",
            alias="default"  # Permite usar múltiples conexiones si es necesario
        )
        print("✅ Conexión a MongoDB establecida con éxito.")
    except Exception as e:
        print(f"❌ Error al conectar a MongoDB: {e}")


