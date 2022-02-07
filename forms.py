from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SelectField, SubmitField, validators, DateField
from wtforms.validators import DataRequired
# from flask.ext.admin.form import widgets

class NewTask(FlaskForm):
    name = StringField("Task Name", validators = [DataRequired()])
    user_options = [("", ""), (1, "Mark"), (2, "Kate"), (3, "Andrew"), (4, "Elizabeth")]
    user_id = SelectField("Assigned to:", choices = user_options, validate_choice=False)
    date = DateField('Due by', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField("Add New Task")

class DelTask(FlaskForm):
    name = StringField("Task Name", validators = [DataRequired()])
    submit = SubmitField("Delete Task")