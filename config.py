from decouple import config


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = config("SECRET_KEY", default="supersecretkey")
    SECURITY_PASSWORD_SALT = config("SECURITY_PASSWORD_SALT", default="somesecretsalt")

    # Mail Settings
    MAIL_DEFAULT_SENDER = "admin@admin.com"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = config("EMAIL_USER")
    MAIL_PASSWORD = config("EMAIL_PASSWORD")
