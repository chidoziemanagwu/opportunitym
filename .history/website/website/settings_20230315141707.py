import os
from pathlib import Path

from dotenv import load_dotenv

import pymysql #MD I added this because the server would not run on MAC
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    # 'django-env-Real-repo.eba-drc3hyss.eu-west-2.elasticbeanstalk.com',
    'webapp-17-10-2022-env.eba-26murmx7.eu-west-2.elasticbeanstalk.com'#new
    'django-env-Website-repo.eba-rpasqmk6.eu-west-2.elasticbeanstalk.com',
    'localhost',
    '127.0.0.1',
    '13.41.26.131',
    '18.168.156.15',
    'olivermccourty.com',
    'www.olivermccourty.com',
    'ec2-18-168-156-15.eu-west-2.compute.amazonaws.com',
    'ec2-3-8-86-171.eu-west-2.compute.amazonaws.com',
    'ec2-13-40-155-126.eu-west-2.compute.amazonaws.com',
    '172.31.8.254',
    '13.40.155.126',
    #new
    '18.170.88.231',
    'ec2-18-170-88-231.eu-west-2.compute.amazonaws.com',
    #new
    'website-checking-env.eba-fsriar6p.eu-west-2.elasticbeanstalk.com',
    'smtpout.olivermccourty.com',
    'opportunitym.com',
    'www.opportunitym.com'
    '*'
]


# Application definition

INSTALLED_APPS = [
    'users',
    'base.apps.BaseConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'payment',
    'paypal.standard.ipn',
    'ckeditor',
    'ckeditor_uploader',
    "verify_email.apps.VerifyEmailConfig",
    "admin_honeypot",
    'django_advanced_password_validation',
    # "cities",
    # "django.contrib.gis",

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates').replace('\\', '/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'my_templatetag': 'base.templatetags.templatetagname'
            }
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# * local database storage
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# ! run this in aws server -----> yum install mysql-devel
# * aws Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASES_NAME'),
        'USER': os.getenv('DATABASES_USER'),
        'PASSWORD': os.getenv("DATABASES_PASSWORD"),
        'HOST': 'database-1.cjgquunsohhw.eu-west-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
    {
        'NAME': 'django_advanced_password_validation.advanced_password_validation.ContainsDigitsValidator',
        'OPTIONS': {
            'min_digits': 1
        }
    },
    {
        'NAME': 'django_advanced_password_validation.advanced_password_validation.ContainsUppercaseValidator',
        'OPTIONS': {
            'min_uppercase': 1
        }
    },
    {
        'NAME': 'django_advanced_password_validation.advanced_password_validation.ContainsLowercaseValidator',
        'OPTIONS': {
            'min_lowercase': 1
        }
    },
    {
        'NAME': 'django_advanced_password_validation.advanced_password_validation.ContainsSpecialCharactersValidator',
        'OPTIONS': {
            'min_characters': 1
        }
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# AWS S3 setting # # # # # # # # # # # # # # # # # # # # # #

AWS_S3_ACCESS_KEY_ID = os.getenv('AWS_S3_ACCESS_KEY_ID')

AWS_S3_SECRET_ACCESS_KEY = os.getenv('AWS_S3_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

AWS_DEFAULT_ACL = 'public-read'

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400'
}

AWS_LOCATION = 'static'

AWS_QUERYSTRING_AUTH = False

AWS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# *Local static
# STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]


# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# * AWS Static


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
STATIC_ROOT = STATIC_URL

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
MEDIA_ROOT = MEDIA_URL

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_ENDPOINT_SECRET = os.getenv('STRIPE_ENDPOINT_SECRET')

# Paypal setting
PAYPAL_TEST = True

PAYPAL_RECEIVER_EMAIL = 'youremail@mail.com'

# ckeditor upload setting 
# * aws CKEDITOR_BASEPATH
CKEDITOR_BASEPATH = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/ckeditor/ckeditor/'

# * local CKEDITOR_BASEPATH
# CKEDITOR_BASEPATH = '/static/ckeditor/ckeditor/'

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'width': 680,
        'extraPlugins': ','.join(['codesnippet',
                                  'html5video',
                                  'widget',
                                  'widgetselection',
                                  'clipboard',
                                  'lineutils'
                                  ]),
    },
}
X_FRAME_OPTIONS = 'SAMEORIGIN'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@opportunitym.com'
EMAIL_HOST_PASSWORD = 'syrt zamf khpv mavs'
DEFAULT_FROM_EMAIL = 'no-reply@opportunitym.com'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
# SUBJECT = 'OpportunityM - Contact'

#EMAIL_PORT = 465

#EMAIL VERIFICATION PAGES
HTML_MESSAGE_TEMPLATE = "registration/verification_email_template.html"
VERIFICATION_SUCCESS_TEMPLATE = "registration/success_email.html"
VERIFICATION_FAILED_TEMPLATE = "registration/fail_verification.html"
REQUEST_NEW_EMAIL_TEMPLATE = "registration/resend_verification.html"
LINK_EXPIRED_TEMPLATE = "registration/linkexpired.html"
NEW_EMAIL_SENT_TEMPLATE  = "registration/new_email_sent.html"
FAIL_NEW_EMAIL_SENT_TEMPLATE  = 'fail_new_email_sent'
LOGIN_URL = 'user_login_page'
MAX_RETRIES = 10

# GDAL_LIBRARY_PATH = '/opt/homebrew/opt/gdal/lib/libgdal.dylib'
# GEOS_LIBRARY_PATH = '/opt/homebrew/opt/geos/lib/libgeos_c.dylib'
# 
# APPEND_SLASH=False