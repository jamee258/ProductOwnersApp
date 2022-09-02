from flask_wtf import FlaskForm
from wtforms import (StringField, SelectField, SelectMultipleField)
from wtforms.validators import InputRequired, Length

class ApplicationForm(FlaskForm):
    apps = SelectField('Application Name', validators=[InputRequired()])
    users = SelectMultipleField('Users', validators=[InputRequired()], validate_choice=False)

class EditApplicationForm(FlaskForm):
    app = StringField('Application Name', render_kw={'readonly': True})
    current_product_owners = StringField('Current Product Owners', render_kw={'readonly': True})
    users = SelectMultipleField('Users', validate_choice=False)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),
                                             Length(min=2, max=200)])
    password = StringField('Password', validators=[InputRequired(),
                                             Length(min=2, max=200)])