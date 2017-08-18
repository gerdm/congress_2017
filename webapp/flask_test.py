from flask import Flask, redirect, render_template, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

# Tell Flask where to look the 'working files'
app = Flask(__name__)
app.config["SECRET_KEY"] = "1F9HClu5BiUu5MT6xvAf"

# Provides CLI properties when debugging the webapp
manager = Manager(app)
bootstrap = Bootstrap(app)

class NameForm(FlaskForm):
    first_name = StringField("First Name", validators=[Required()])
    last_name = StringField("Last name", validators=[Required()])
    secret_code = StringField("Secret Code", validators=[Required()])
    submit = SubmitField("Submit")

@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
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
