from flask import jsonify, render_template, redirect, url_for, session, request, flash
from . import main
from .forms import MembersForm
from .. import db
from ..models import Round_Table, Workshop, Grade
from flask_login import login_required

@main.route("/_get_tables/")
def _get_tables():
    grade  = request.args.get("grade", 1, type=int)
    tables = [(row.id, row.table) for row in
              Round_Table.query.filter_by(grade_allowed=grade).all()]
    return jsonify(tables)

@main.route("/_get_workshops/")
def _get_workshops():
    grade  = request.args.get("grade", 1, type=int)
    workshops = [(row.id, row.workshop) for row in
              Workshop.query.filter_by(grade_allowed=grade).all()]
    return jsonify(workshops)

@main.route("/", methods=["GET", "POST"])
def index():
    form = MembersForm()
    form.grade.choices = [(row.id, row.name) for row in Grade.query.all()]
    form.round_table.choices = [(row.id, row.table) for row in Round_Table.query.all()]
    form.workshop.choices = [(row.id, row.workshop) for row in Workshop.query.all()]
    if form.validate_on_submit():
        session["first_name"] = form.first_name.data
        flash("Thank you for signing in {}!".format(session.get("first_name")))
        return redirect(url_for(".index"))
    return render_template("index.html", form=form)

@main.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)

# The 'redirect' method allows the webpage to take you
# to another page and return a 302 response: redirect
@main.route("/redirect")
@login_required
def goto_github():
    return redirect("https://github.com/gerdm")

