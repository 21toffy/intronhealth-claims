from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, TextAreaField, IntegerField, DateField, DateTimeField
from wtforms import validators
from app.models import User

# all_users = User.query.with_entities(User.full_name).all()


class AddUser(FlaskForm):
    name = StringField('name', validators=[validators.length(min=3, max=100), validators.DataRequired()])
    gender = RadioField('gender', choices = ['male', 'female'])
    salary = IntegerField(validators=[validators.NumberRange(min=0), validators.DataRequired()])
    date_of_birth = DateField(format='%Y-%m-%d', validators=[validators.DataRequired()])


class ClaimForm(FlaskForm):
    user = SelectField('User', validators=[validators.DataRequired()])
    diagnosis = TextAreaField('Diagnosis', validators=[validators.DataRequired()])
    hmo = SelectField('HMO', choices=[('HMO1', 'HMO1'), ('HMO2', 'HMO2'), ('HMO3', 'HMO3'), ('HMO4', 'HMO4')], validators=[validators.DataRequired()])
    age = IntegerField('Age', validators=[validators.DataRequired()])
    
    service_date = DateField('Service Date', validators=[validators.DataRequired()])
    service_name = StringField('Service Name', validators=[validators.DataRequired()])
    service_type = RadioField('Service Type', choices=[('Hematology', 'Hematology'), ('Microbiology', 'Microbiology'), ('Chemical Pathology', 'Chemical Pathology'), ('Histopathology', 'Histopathology'), ('Immunology', 'Immunology')], validators=[validators.DataRequired()])
    provider_name = StringField('Provider Name', validators=[validators.DataRequired()])
    source = StringField('Source', validators=[validators.DataRequired()])
    cost_of_service = StringField('Cost of Service', validators=[validators.DataRequired()])