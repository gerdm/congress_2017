from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import Required

class MembersForm(FlaskForm):
    first_name = StringField("Nombre", validators=[Required()])
    last_name_father = StringField("Apellido Paterno", validators=[Required()])
    last_name_mother = StringField("Apellido Materno", validators=[Required()])
    email = StringField("Email", validators=[Required()])
    school = StringField("Escuela", validators=[Required()])
    # Dinamyc creation of the form for grade and workshop: setting the data afterwards
    grade = SelectField("Grado de Estudio", coerce=int, id="select_grade")
    round_table = SelectField("Selecciona la mesa rendonda a atender", coerce=int, id="select_table")
    secret_code = StringField("Validación de código", validators=[Required()])
    submit = SubmitField("Enviar")

class SignUser(FlaskForm):
    day = SelectField("Día a registrar", choices=[(1, "Ingreso Día 1"), (2, " Ingreso Día 2"),
                                                  (3, "Comida Día 1"), (4, "Comida Día 2")],
                      coerce=int, id="select_day")
    submit = SubmitField("Registrar")
