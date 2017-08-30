from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
# Importing the blueprint
from . import auth
from .forms import LoginForm
from ..models import Manager


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        manager = Manager.query.filter_by(email=form.email.data).first()
        if manager is not None and manager.verify_password(form.password.data):
            login_user(manager, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash("Invalid Username or Password")
    # Access in templates/auth/login.html
    return render_template("auth/login.html", form=form)

