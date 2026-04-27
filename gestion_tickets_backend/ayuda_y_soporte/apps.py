from django.apps import AppConfig

class AyudaYSoporteConfig(AppConfig):
    # El campo por defecto para claves primarias será BigAutoField, lo cual es adecuado para manejar un gran número de registros
    default_auto_field = 'django.db.models.BigAutoField'
    
    # El nombre de la aplicación, que debe coincidir con el nombre del directorio donde se encuentra la aplicación
    name = 'ayuda_y_soporte'
