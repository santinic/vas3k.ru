import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = "wow so secret"
DEBUG = False
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ["vas3k.ru", "thedevel.ru"]

INSTALLED_APPS = (
    "django.contrib.staticfiles",
    "stories",
    "comments"
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
)

ROOT_URLCONF = "vas3k.urls"

WSGI_APPLICATION = "vas3k.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "vas3kru",
        "USER": "vas3k",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",

    # my
    "stories.context_processors.settings.settings_processor",
    "stories.context_processors.cookies.cookies_processor",
    "comments.context_processors.comments.last_comments_processor"
)

LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = False
STATIC_URL = "/static/"

IMAGE_UPLOAD_PATH = os.path.join(BASE_DIR, "upload/images")
MAIN_PAGE_SIZE = 20
STORIES_LIST_PAGE_SIZE = {
    "blog": 16,
    "gallery": 36
}
STORIES_LIST_DEFAULT_PAGE_SIZE = 30
TITLE = "vas3k.ru"
BIG_TEMPLATES = ["blog", "gallery"]
SMALL_TEMPLATES = ["pictwitter", "pictwitterbig", "foursquare", "instagram", "text"]
CUSTOM_AVATARS = ["vas3k", "themylogin", "redetection"]

GOOGLE_MAPS_API_KEY = ""

try:
    from vas3k.private_settings import *
except ImportError:
    pass

try:
    from vas3k.local_settings import *
except ImportError:
    pass
