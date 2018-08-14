from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Length, DataRequired
from wtforms_components import TimeField


class LoginFormView(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=5, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=80)])
    remember = BooleanField('remember me')


class AddRuteForm(FlaskForm):
    dari = StringField('Dari', validators=[DataRequired()])
    tujuan = StringField('Tujuan', validators=[DataRequired()])
    ongkos = IntegerField('Ongkos', validators=[DataRequired()])
    tanggal_keberangkatan = DateField('Tanggal Keberangkatan', format='%Y-%m-%d', validators=[DataRequired()])
    jam = TimeField('Jam', validators=[DataRequired()])
    jumlah_kursi = IntegerField('Ongkos', validators=[DataRequired()])

class EditRuteForm(FlaskForm):
    dari = StringField('Dari', validators=[DataRequired()])
    tujuan = StringField('Tujuan', validators=[DataRequired()])
    ongkos = IntegerField('Ongkos', validators=[DataRequired()])
    tanggal_keberangkatan = DateField('Tanggal Keberangkatan', format='%Y-%m-%d', validators=[DataRequired()])
    jam = TimeField('Jam', validators=[DataRequired()])
    jumlah_kursi = IntegerField('Ongkos', validators=[DataRequired()])