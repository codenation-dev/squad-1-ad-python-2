from .settings import *
import dj_database_url


DEBUG = False

# procura pela URL do banco em DATABASE_URL
DATABASES = {
    'default': dj_database_url.config()
}

# https://devcenter.heroku.com/articles/django-assets
# Django and Static Assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

#MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
