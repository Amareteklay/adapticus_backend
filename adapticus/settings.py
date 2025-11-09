from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security / Debug
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-insecure-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "127.0.0.1,localhost,amareteklay.eu.pythonanywhere.com"
).split(",")

# --- Apps
INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",

    # third-party
    "rest_framework","drf_spectacular","corsheaders","parler",

    # our apps
    "core","taxonomy","content","portfolio","salon",
]

# --- Middleware (CORS first)
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", 
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


ROOT_URLCONF = "adapticus.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ],},
}]

WSGI_APPLICATION = "adapticus.wsgi.application"

# --- DB
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- Auth
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- i18n
LANGUAGE_CODE = "en"
TIME_ZONE = "Europe/Stockholm"
USE_I18N = True
USE_TZ = True

LANGUAGES = (
    ("en", "English"),
    ("ti-et", "Tigrinya"),
    ("sv", "Swedish"),
)

PARLER_DEFAULT_LANGUAGE = "en"
PARLER_LANGUAGES = {
    None: (
        {"code": "en"},
        {"code": "sv"},
        {"code": "ti-et"},
    ),
    "default": {
        "fallbacks": ["en"],
        "hide_untranslated": False,
    },
}

# --- Static / Media
STATIC_URL = "/static/"                      
STATIC_ROOT = BASE_DIR / "staticfiles"       
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- DRF
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 12,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Adapticus API",
    "VERSION": "1.0.0",
}

# --- CORS / CSRF (frontends on Vercel + custom domains)
CORS_ALLOWED_ORIGINS = [
    "https://amareteklay.com",
    "https://www.amareteklay.com",
    "https://homoadapticus.com",
    "https://www.homoadapticus.com",
    "https://amareteklay.vercel.app",
    "https://homoadapticus.vercel.app",
]
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https:\/\/[a-z0-9-]+\.vercel\.app$",
]
# CORS_ALLOW_CREDENTIALS = True  # enable if you ever send cookies

CSRF_TRUSTED_ORIGINS = [
    "https://amareteklay.com",
    "https://www.amareteklay.com",
    "https://homoadapticus.com",
    "https://www.homoadapticus.com",
    "https://amareteklay.vercel.app",
    "https://homoadapticus.vercel.app",
]
