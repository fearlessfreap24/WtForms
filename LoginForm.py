from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(),Length(min=5, max=20, message="Must be between 5 and 20 characters")])
    # email = StringField('Email Address', validators=[InputRequired(), Email('An email address is required')])

