from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length


class LoginFormView(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=5, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=80)])
    remember = BooleanField('remember me')