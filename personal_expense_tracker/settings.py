from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = "django-insecure-your-secret-key-here"


DEBUG = True


ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

INSTALLED_APPS = [

    "jazzmin",

    "django.contrib.admin",

    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "widget_tweaks",

    "expenses.apps.ExpensesConfig",
]

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]

ROOT_URLCONF = "personal_expense_tracker.urls"

TEMPLATES = [
    {
        "BACKEND":
        "django.template.backends.django.DjangoTemplates",

        "DIRS":
        [BASE_DIR / "templates"],

        "APP_DIRS":
        True,

        "OPTIONS":
        {
            "context_processors":
            [
                "django.template.context_processors.debug",

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "personal_expense_tracker.wsgi.application"

DATABASES = {

    "default": {

        "ENGINE":
        "django.db.backends.sqlite3",

        "NAME":
        BASE_DIR / "db.sqlite3",

    }

}

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },

]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

STATICFILES_DIRS = [

    BASE_DIR / "static",

]

STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/accounts/login/"

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)

JAZZMIN_SETTINGS = {

    "site_title": "Expense Tracker",

    "site_header": "Personal Expense Tracker",

    "site_brand": "Expense Tracker",

    "site_logo": None,

    "welcome_sign": "Welcome to Personal Expense Tracker",

    "copyright": "© 2026 Arnav Baxi",

    "search_model": [
        "auth.User",
        "expenses.Expense",
        "expenses.Category",
        "expenses.Budget",
        "expenses.UserProfile",
    ],

    "show_sidebar": True,

    "navigation_expanded": True,

    "hide_apps": [],

    "hide_models": [],

    "order_with_respect_to": [
        "expenses",
        "auth",
    ],

    "icons": {
        "auth.user": "fas fa-user",
        "auth.group": "fas fa-users",

        "expenses.expense": "fas fa-wallet",

        "expenses.category": "fas fa-tags",

        "expenses.budget": "fas fa-coins",

        "expenses.userprofile": "fas fa-user-circle",
    },

    "changeform_format": "horizontal_tabs",

    "language_chooser": False,
}