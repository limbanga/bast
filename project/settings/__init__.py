from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # my apps
    "app",
    "ckeditor",
    # Django Allauth
    "django.contrib.sites",  # Yêu cầu bởi Allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",  # Chỉ cần nếu dùng đăng nhập mạng xã hội
    "allauth.socialaccount.providers.google",  # Thêm provider bạn cần
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Thêm middleware của allauth
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR / "templates/app",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGIN_URL = "/auth/login"

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": [
            ["Format", "Bold", "Italic", "Underline", "Strike", "SpellChecker"],
            [
                "NumberedList",
                "BulletedList",
                "Indent",
                "Outdent",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
            ],
            [
                "Image",
                "Table",
                "Link",
                "Unlink",
                "Anchor",
                "SectionLink",
                "Subscript",
                "Superscript",
            ],
            ["Undo", "Redo"],
            ["Source"],
            ["Maximize"],
        ],
        "height": 220,
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # Django auth backend
    "allauth.account.auth_backends.AuthenticationBackend",  # Allauth backend
]


# # Tự động xác minh email (True/False)
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"

# # Yêu cầu email duy nhất cho mỗi tài khoản
# ACCOUNT_UNIQUE_EMAIL = True

# # Xác định trường đăng nhập (email hoặc username)
# ACCOUNT_AUTHENTICATION_METHOD = "email"  # Hoặc "username_email", "username"

# # Cho phép người dùng đăng ký
# ACCOUNT_SIGNUP_ENABLED = True

# Tắt xác nhận email khi người dùng đăng ký
ACCOUNT_EMAIL_VERIFICATION = "none"

# Tắt gửi email thông báo khi tài khoản được tạo
ACCOUNT_EMAIL_REQUIRED = False

# Đặt email làm trường đăng nhập chính
ACCOUNT_AUTHENTICATION_METHOD = "email"

# Đảm bảo email là trường duy nhất để đăng nhập
ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_FORMS = {
    "signup": "app.forms.SignupFormz",
    "login": "app.forms.LoginFormz",
    "reset_password": "app.forms.ResetPasswordFormz",
        'change_password': 'app.forms.ChangePasswordFormz',

}

# Đảm bảo cấu hình các URLs liên quan
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "key": "",
        }
    }
}

LOGIN_REDIRECT_URL = "/"  # URL mà bạn muốn redirect


print("BASE_DIR", BASE_DIR)


if DEBUG:
    from .development import *
else:
    from .production import *
