from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class data_input(FlaskForm):
    equation = StringField('Enter Objective, Constraints', validators=[DataRequired()])
    submit = SubmitField('Compute')
