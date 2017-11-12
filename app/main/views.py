from flask import jsonify, render_template, redirect, url_for, session, request, flash
from ..models import Round_Table, Workshop, Grade, User, Passcode
from .forms import MembersForm, SignUser, GiveFood
from flask_login import login_required
from . import main
from .. import db

import pyqrcode as qr
from io import BytesIO
from PIL import Image, ImageDraw
from flask import send_file
import base64


@main.route("/extract_name/<id>", methods=["POST"])
def extract_name(id):
    url_user = url_for(".user", username_id=id, _external=True)
    qr_pass = qr.create(url_user)
    qr_save = BytesIO()
    qr_pass.png(qr_save, scale=20)
    qr_save.seek(0)
    qr_png = base64.b64encode(qr_save.getvalue())

    user_name = User.query.filter_by(id=id).first().first_name
    return render_template("outputqr.html", result=qr_png.decode("utf8"),
                           name=user_name)

@main.route("/", methods=["GET", "POST"])
def index():
    form = MembersForm()
    form.grade.choices = [(row.id, row.name) for row in Grade.query.all()]
    form.round_table.choices = [(row.id, row.table) for row in Round_Table.query.all()
                                if row.available_position > 0]
    if form.validate_on_submit():
        validate_pass = Passcode.query.filter_by(passes=form.secret_code.data)
        if bool(validate_pass.first()):
            session["first_name"] = form.first_name.data
            round_table_id = form.round_table.data
            new_user = User(
                    first_name=form.first_name.data,
                    last_name_father=form.last_name_father.data,
                    last_name_mother=form.last_name_mother.data,
                    email=form.email.data,
                    school=form.school.data,
                    grade_id=form.grade.data,
                    round_table_id=round_table_id,
                    day1=False,
                    day2=False)

            # Add User to database
            db.session.add(new_user)
            # Delete passcode from database
            validate_pass.delete()
            # Remove one available position
            Round_Table.query.filter_by(id=round_table_id).first().available_position -= 1
            # and update database
            db.session.commit()
            user_id = new_user.id

            return redirect(url_for(".extract_name", id=user_id), code=307)
        else:
            flash("¡Código no valido!")
    return render_template("index.html", form=form)

@main.route("/user/<username_id>", methods=["GET", "POST"])
@login_required
def user(username_id):
    user = User.query.filter_by(id=username_id).first()
    query = ("SELECT workshop "
            "FROM workshops, school_grades, users "
             "WHERE workshops.id = school_grades.workshop_id AND "
                    "school_grades.id = users.grade_id AND "
                    "users.id = {}".format(username_id))
    user_workshop = list(db.engine.execute(query))[0][0]
    formd = SignUser()
    if formd.validate_on_submit():
        if formd.day.data == 1:
            user.day1 = True
        elif formd.day.data == 2:
            user.day2 = True
        elif formd.day.data == 3:
            user.food1 = True
        elif formd.day.data == 4:
            user.food2 = True

    return render_template("user.html", user=user, formd=formd,
                           user_workshop=user_workshop)

# The 'redirect' method allows the webpage to take you
# to another page and return a 302 response: redirect
@main.route("/redirect")
@login_required
def goto_github():
    return redirect("https://github.com/gerdm")

