DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql://nadia:12345@service_postgresql_di_dalam_docker/nadia_tiket'
DATABASE_FILE = SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = '12345'

#############################################################################################################
# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
#############################################################################################################

#############################################################################################################

#twilio
# Your Account SID from twilio.com/console

# this upgraded SID for user
TWLIO_ACCOUNT_SID_UPGRADED_FOR_USER = "YOUR_TWILIO_SID"

# this non upgrade SID for admin
TWLIO_ACCOUNT_SID_NONE_UPGRADED_FOR_ADMIN = "YOUR_TWILIO_SID"


# Your Auth Token from twilio.com/console

# this upgraded auth_token for user
TWLIO_AUTH_TOKEN_UPGRADED_FOR_USER = "YOUR_TWILIO_AUTH_TOKEN"

# this none upgraded auth_token for admin
TWLIO_AUTH_TOKEN_NONE_UPGRADED_FOR_ADMIN = "YOUR_TWILIO_AUTH_TOKEN"

#############################################################################################################

#############################################################################################################
PDF_FOLDER = 'web_app/files/pdf/'
TEMPLATE_FOLDER = 'web_app/templates/'
#############################################################################################################

