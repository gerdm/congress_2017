from flask import jsonify, render_template, redirect, url_for, session, request, flash
from . import main
from .forms import MembersForm, SignUser
from .. import db
from ..models import Round_Table, Workshop, Grade, Beverage, User
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
    form.beverage.choices = [(row.id, row.beverage) for row in Beverage.query.all()]
    if form.validate_on_submit():
        session["first_name"] = form.first_name.data
        new_user = User(
                first_name = form.first_name.data,
                last_name_father = form.last_name_father.data,
                last_name_mother = form.last_name_mother.data,
                email = form.email.data,
                school = form.school.data,
                grade_id = form.grade.data,
                beverage_id = form.beverage.data,
                workshop_id = form.workshop.data,
                round_table_id = form.round_table.data,
                kit=False
                )
        db.session.add(new_user)

        flash("Thank you for signing in {}!".format(sessio.get("first_name")))
        return redirect(url_for(".index"))
    return render_template("index.html", form=form)

@main.route("/user/<username_id>", methods=["GET", "POST"])
@login_required
def user(username_id):
    user = User.query.filter_by(id=username_id).first()
    form = SignUser()
    if form.validate_on_submit():
        user.kit = True
        return render_template("user.html", user=user, form=form)
    return render_template("user.html", user=user, form=form)

# The 'redirect' method allows the webpage to take you
# to another page and return a 302 response: redirect
@main.route("/redirect")
@login_required
def goto_github():
    return redirect("https://github.com/gerdm")

