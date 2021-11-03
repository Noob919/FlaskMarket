from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo,Email, DataRequired, ValidationError

from flaskmarket.models import User

class RegistrationForm(FlaskForm):

    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username exit! Please try something different")

    def validate_email_address(self,email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError("Email exit! Please use different email")

    username = StringField(label = 'username', validators = [Length(min=2, max=20), DataRequired()])
    email_address  = StringField(label = 'email_address', validators = [Email(), DataRequired()])
    password1 = PasswordField(label = 'password1', validators = [Length(min=6), DataRequired()])
    password2 = PasswordField(label = 'password2', validators= [EqualTo('password1'), DataRequired()])
    submit = SubmitField(label = 'Create Account')

class LoginForm(FlaskForm):
    username = StringField(label = 'username', validators = [DataRequired()])
    password = PasswordField(label = 'password', validators = [DataRequired()])
    submit = SubmitField(label = 'Sign in')

class PurchaseForm(FlaskForm):
    submit = SubmitField(label = 'Purchase Item!')

class SellForm(FlaskForm):
    submit = SubmitField(label = 'Sell Item!')