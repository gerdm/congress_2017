from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
# Importing the blueprint
from . import auth
from .forms import LoginForm
from ..models import Staff


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        staff = Staff.query.filter_by(email=form.email.data).first()
        if staff is not None and staff.verify_password(form.password.data):
            login_user(staff, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash("Invalid Username or Password")
    # Access in templates/auth/login.html
    return render_template("auth/login.html", form=form)


@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You have been log out!")
    return redirect(url_for("main.index"))
