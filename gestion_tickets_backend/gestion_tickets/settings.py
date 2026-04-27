"""
Configuración de Django para el proyecto de Gestión de Tickets.
"""

from pathlib import Path  # Para manejar rutas dentro del proyecto
import mongoengine  # MongoEngine para conectar con MongoDB
import os  # Para manejar variables de entorno del sistema
from datetime import timedelta  # Para manejar expiración de tokens JWT
from decouple import config  # Para leer variables del .env
from dotenv import load_dotenv  # Para cargar archivo .env

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Definimos la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta usada por Django (¡cambiarla en producción!)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'cambiar-esto-en-produccion')

# Activar o desactivar el modo DEBUG (desactívalo en producción)
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Lista de hosts permitidos (modifícalo en producción)
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Configuración de conexión con MongoDB (solo usamos MongoDB)
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'ticketsdb')
MONGO_URI = os.getenv('MONGO_URI', f'mongodb://127.0.0.1:27017/{MONGO_DB_NAME}')

# Intentamos conectar a MongoDB con MongoEngine
try:
    mongoengine.connect(db=MONGO_DB_NAME, host=MONGO_URI)
    print("Conexión a MongoDB establecida correctamente desde settings.py")
except Exception as e:
    print(f" Error al conectar a MongoDB: {e}")

# Configuración dummy para DATABASES (evita que Django busque una base SQL relacional)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

# Aplicaciones instaladas en el proyecto
INSTALLED_APPS = [
    'django.contrib.admin',        # Admin de Django (usado solo si se habilita, aunque no administres usuarios aquí)
    'django.contrib.auth',         # Sistema de auth (no se usa directamente pero algunas apps dependen de él)
    'django.contrib.contenttypes', # Tipos de contenido
    'django.contrib.sessions',     # Manejo de sesiones
    'django.contrib.messages',     # Sistema de mensajes
    'django.contrib.staticfiles',  # Archivos estáticos
    'rest_framework',              # Django REST Framework
    'rest_framework_simplejwt',    # JWT con DRF
    'corsheaders',                 # Para permitir peticiones desde el frontend
    'django_extensions',           # Utilidades para desarrollo
    # Tus aplicaciones personalizadas
    'usuarios',
    'tickets',
    'ayuda_y_soporte',
    'reportes',
    'saldo',
    'comprar_horas',
    'departamentos',
]

# Middleware de Django
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Middleware para CORS (habilita conexión con el frontend)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración del backend de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Puedes agregar aquí rutas a tus templates si los usas
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuración de la URL raíz (archivo urls.py principal)
ROOT_URLCONF = 'gestion_tickets.urls'


# Configuración del archivo WSGI
WSGI_APPLICATION = 'gestion_tickets.wsgi.application'

# Configuración del lenguaje y zona horaria
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Ruta de archivos estáticos (CSS, JS, etc.)
STATIC_URL = '/static/'

# Configuración de Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'usuarios.authentication.MongoDBJWTAuthentication',  # Autenticación personalizada usando MongoEngine
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Fallback de autenticación JWT estándar
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Por defecto, se requiere autenticación
    ),
}

# Configuración de JWT (usado para acceso seguro desde frontend)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),  # Duración del access token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Duración del refresh token
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# Configuración de CORS para permitir peticiones desde tu frontend en React
CORS_ALLOW_ALL_ORIGINS = True  # Solo en desarrollo. En producción usar CORS_ALLOWED_ORIGINS

CORS_ALLOW_CREDENTIALS = True  # Permitir cookies si es necesario

# Métodos HTTP permitidos en CORS
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
]

# Headers permitidos en las peticiones desde el frontend
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Configuración de correo electrónico (para recuperación de contraseña, etc.)
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# Email que aparece como remitente en los correos enviados
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
