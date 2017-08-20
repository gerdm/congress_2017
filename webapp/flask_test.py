from flask import Flask, redirect, render_template, flash
from flask_script import Manager
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

class MembersForm(FlaskForm):
    first_name = StringField("First Name", validators=[Required()])
    last_name = StringField("Last name", validators=[Required()])
    workshop = SelectField("Worksop",
                           choices=[("conf1", "Conference 1"),  ("conf2", "Conference 2"), ("conf3", "Conference 3")])
    secret_code = StringField("Secret Code", validators=[Required()])
    submit = SubmitField("Submit")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/", methods=["GET", "POST"])
def index():
    form = MembersForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        form.first_name.data = ""
        form.last_name.data = ""
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
