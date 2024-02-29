from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,PasswordField
from wtforms.validators import DataRequired,Email,EqualTo

class RegistrationForm(FlaskForm):
    username= StringField('Username',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('password',validators=[DataRequired()])
    repeat_password=PasswordField('repeat_password', validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField()

class LoginFOrm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me=BooleanField('remember_me')
    submit = SubmitField()

class Posts(FlaskForm):
    text  = StringField('Text', validators=[DataRequired()])
    submit = SubmitField()

class Coments(FlaskForm):
    text  = StringField('Text', validators=[DataRequired()])
    submit = SubmitField()

class LoginFOrm1(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me=BooleanField('remember_me')
    submit = SubmitField()

