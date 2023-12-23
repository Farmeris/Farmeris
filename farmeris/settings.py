# settings.py
from django.utils.translation import gettext_lazy as _
from pathlib import Path
import os
import json
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    #google
    # The following apps are required:
    'django.contrib.sites',
    #tailwind styling
    "allauth_ui",
    "widget_tweaks",
    #authorization
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    #'allauth.socialaccount.providers.github',
    #'allauth.socialaccount.providers.gitlab',
    'allauth.socialaccount.providers.google',
    #'allauth.socialaccount.providers.instagram',
    #'allauth.socialaccount.providers.facebook',
    #end of google auth via allauth
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'login_app.apps.LoginAppConfig',
    'login_app',
    'add_product',
    'user_profile',
    'add_product_main',
    'edit_profile',
    'chat_polozka',
    'search',
    'obrazky',
    'chat_general',
    'main',
    'email_verification',
]

SITE_ID = 1

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

env = environ.Env()
# Reading .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.elasticsearch5_backend.Elasticsearch5Sear$
#        'URL': 'http://localhost:9200/',
#        'INDEX_NAME': 'my_index',
#    },
#}


LOGIN_URL = 'login'  # Specify the URL name of your login page

MIDDLEWARE = [
    #'csp.middleware.CSPMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #color theme
    'login_app.middlewares.theme_switch_middleware',
    'add_product_main.middlewares.SetUserPreferredLanguageMiddleware',
    'language.DefaultLanguageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'add_product_main.middleware.UpdateFilterTrustedMiddleware',
]

LANGUAGES = [
    ('sk', _('Slovak')),
#    ('cz', _('Czech')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

ROOT_URLCONF = 'farmeris.urls'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

#google_oauth_pointer_path = os.path.join(BASE_DIR, ".secret", "google_oauth.json")
#try:
#    with open(google_oauth_pointer_path, "r") as pointer_file:
#        oauth_path_data = json.load(pointer_file)
#        google_oauth_actual_path = os.path.join(BASE_DIR, oauth_path_data["GOOGLE_OAUTH_PATH"])
#except FileNotFoundError:
#    raise Exception("Could not find google_oauth.json. Check your paths!")
#
#with open(google_oauth_actual_path, "r") as oauth_file:
#    google_credentials = json.load(oauth_file)
#
#SOCIALACCOUNT_PROVIDERS = {
#    'google': {
#        'APP': {
#            'client_id': google_credentials["web"]["client_id"],
#            'secret': google_credentials["web"]["client_secret"],
#            'key': ''  # If you don't have a key, just leave it as an empty string
#        }
#    }
#}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'add_product_main.context_processors.user_preferred_language',
                'user_profile.context_processors.user_stats',
                'user_profile.context_processors.css_styles',
                # that contains the 'context_processors.py' file.
                'django.template.context_processors.debug',
                #'allauth.account.context_processors.account',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'edit_profile.context_processors.avatar_processor',
                #color theme
                'login_app.context_processors.theme_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'farmeris.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'sk'
TIME_ZONE = 'Europe/Bratislava'
USE_I18N = True
USE_TZ = True
DECIMAL_PLACES = 4
USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'common_static'),
    os.path.join(BASE_DIR, "templates/static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Safety as strong as Arnie
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ['https://*.farmeris.sk', 'https://farmeris.sk']
CSRF_COOKIE_DOMAIN = '.farmeris.sk'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

LOGIN_REDIRECT_URL = "/main"
LOGOUT_REDIRECT_URL = "/main"

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': env('GOOGLE_CLIENT_ID'),
            'secret': env('GOOGLE_SECRET'),
            'key': env('GOOGLE_KEY', default='')  # If you don't have a key, just leave it as an empty string
        },
        "SCOPE": {
            "profile",
            "email"
        },
        "AUTH_PARAMS": {
            "access_type": "online"
        }
    }
}

#ACCOUNT_FORMS = {
#    'signup': 'login_app.forms.CustomSignupForm',
#}
#email
#SOCIALACCOUNT_ADAPTER = 'login_app.adapters.CustomSocialAccountAdapter'
#ACCOUNT_ADAPTER = 'login_app.adapters.CustomAccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_UNIQUE_EMAIL = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'account_email_verification_sent'
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')  
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')  
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL') 
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# Local debug setting
DEBUG = bool(os.environ.get("DEBUG", default=0))

# Local database settings
#DATABASES = {
#    'default': env.db(),
#}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
