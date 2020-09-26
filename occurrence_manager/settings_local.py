from .settings import *

DEBUG = True
PREPEND_WWW = None

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'ocorrence_manager_db'),
        'USER': os.getenv('DB_USER', 'ocorrence_manager_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'qwertyuiop'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
