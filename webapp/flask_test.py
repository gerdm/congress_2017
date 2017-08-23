from flask import Flask, redirect, render_template, flash
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from os.path import abspath, dirname, join

basedir = abspath(dirname(__file__))
dbase_path = "sqlite:///" + join(basedir, "database.sqlite")

# Tell Flask where to look the 'working files'
app = Flask(__name__)
app.config["SECRET_KEY"] = "1F9HClu5BiUu5MT6xvAf"
app.config["SQLALCHEMY_DATABASE_URI"] = dbase_path
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Provides CLI properties when debugging the webapp
manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

## Database Definition
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), unique=False)
    last_name = db.Column(db.String(64), unique=False)
    school = db.Column(db.String(64), unique=False)
    kit = db.Column(db.Boolean, unique=False)
    grade = db.Column(db.Integer, db.ForeignKey("school_grades.grade"))
    beverage = db.Column(db.Integer, db.ForeignKey("beverages.beverage"))
    user_type = db.Column(db.Integer, db.ForeignKey("user_types.type"))
    workshop = db.Column(db.Integer, db.ForeignKey("workshops.workshop"))
    round_table = db.Column(db.Integer, db.ForeignKey("round_tables.table"))

    def __repr__(self):
        return ("<User {first} {last}>"
                .format(first=self.first_name, last=self.last_name))


class Grade(db.Model):
    __tablename__ = "school_grades"
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<School Grade {grade}>".format(grade=self.grade)


class User_Type(db.Model):
    __tablename__ = "user_types"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<User Type {utype}>".format(utype=self.user_type)


class Beverage(db.Model):
    __tablename__ = "beverages"
    id = db.Column(db.Integer, primary_key=True)
    beverage = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Beverage {beverage}>".format(beverage=self.beverage)


class Workshop(db.Model):
    __tablename__ ="workshops"
    id = db.Column(db.Integer, primary_key=True)
    workshop = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Workshop {ws}>".format(ws=self.workshop)


class Round_Table(db.Model):
    __tablename__ = "round_tables"
    id = db.Column(db.Integer, primary_key=True)
    table = db.Column(db.String)
    users = db.relationship("User", backref="role", lazy="dynamic")
    
    def __repr__(self):
        return "<Round Table {table}>".format(table=self.round_table)

# import the database instance and the models on the run
def make_shell_context():
    return dict(app=app, User=User, Grade=Grade, User_Type=User_Type,
                Beverage=Beverage, Workshop=Workshop, Round_Table=Round_Table)
#manager.add_command("shell", Shell(make_context = make_shell_context))


class MembersForm(FlaskForm):
    first_name = StringField("First Name", validators=[Required()])
    last_name = StringField("Last name", validators=[Required()])
    grade = SelectField("Student Grade",
                        choices=[("g1", "Grade 1"), ("g2", "Grade 2")])
    # Dinamyc creation of the form: setting the data afterwards
    workshop = SelectField("Workshop", coerce=str)
    secret_code = StringField("Secret Code", validators=[Required()])
    submit = SubmitField("Submit")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/", methods=["GET", "POST"])
def index():
    choicesv1 = [("ch1", "Choice 1"), ("ch2", "Choice 2")]
    choicesv2 = [("ch3", "Choice 3"), ("ch4", "Choice 4")]
    form = MembersForm()
    # TODO: Add workshop choices depending on the
    # grade submitted by the user; check if the 
    # workshop is available dependin on the number of people involved
    form.workshop.choices = choicesv1
    if form.validate_on_submit():
        first_name = form.first_name.data
        form.first_name.data = ""
        form.last_name.data = ""
        form.grade.data = ""
        flash("Thank you for signing in {}!".format(first_name))
    return render_template("index.html", form=form)

@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)

# The 'redirect' method allows the webpage to take you
# to another page and return a 302 response: redirect
@app.route("/redirect")
def goto_github():
    return redirect("https://github.com/gerdm")

if __name__ == "__main__":
    #Replaces 'app.run(debug=True)' in order 
    # to give CLI functionalities (see manager)
    manager.run()
