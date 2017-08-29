from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import Required

class MembersForm(FlaskForm):
    first_name = StringField("First Name", validators=[Required()])
    last_name = StringField("Last name", validators=[Required()])
    email = StringField("Email", validators=[Required()])
    # Dinamyc creation of the form for grade and workshop: setting the data afterwards
    grade = SelectField("Student Grade", coerce=int, id="select_grade")
    round_table = SelectField("Round table", coerce=int, id="select_table")
    workshop = SelectField("Workshop", coerce=int, id="select_workshop")
    secret_code = StringField("Secret Code", validators=[Required()])
    submit = SubmitField("Submit")
