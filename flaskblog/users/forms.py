from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flaskblog.models import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

class RegistrationForm(FlaskForm):
    
    username = StringField('Username',
        validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email',
        validators=[DataRequired(), Email()])    
    
    password = PasswordField('Password',
        validators=[DataRequired()])
    
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user: # if user is not null
            raise ValidationError('Username has been registered already.')
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email has been regiestered already.')


class LoginForm(FlaskForm):
    # Can choose email or username for login. Email for now
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
        validators=[DataRequired(), Email()])    
    
    picture = FileField('Update Profile Picture', 
        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username has been taken. Please choose a different one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email has been taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    # check if email exists
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account is using this email. Please register first')

# input 
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')