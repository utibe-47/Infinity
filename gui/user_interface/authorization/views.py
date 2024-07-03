from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user

from . import authorization
from .. import db, primary_users
from ..models import User
from .forms import LoginForm, SignupForm, RequestResetForm, ResetPasswordForm
from ..email_sender import Email


def send_reset_email(user):
    email = Email()
    token = user.get_reset_token()
    subject, sender, recipients = 'Reset UI password', "prod_arp@gam.com", [user.email]
    body = ''' To reset your password, please visit the following link: {}
    Please ignore this email if you did not make this 
    request'''.format(url_for('authorization.reset_token', token=token, _external=True))

    email.send(subject, sender, recipients, body)


@authorization.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.reset_password.data:
        return redirect(url_for('auth.reset_request'))
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(request.args.get('next'))
        flash('Incorrect username or password.')
    return render_template("login.html", form=form)


@authorization.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@authorization.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    primary_user = False
    if form.validate_on_submit():
        if form.email.data in primary_users:
            primary_user = True

        user = User(email=form.email.data, username=form.username.data, password=form.password.data,
                    primary_user=primary_user)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user.username))
        return redirect(url_for('authorization.login'))
    return render_template("signup.html", form=form)


@authorization.route("/reset_request", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to you with instructions on how to reset your password', 'info')
        return redirect(url_for('authorization.login'))

    return render_template("reset_request.html", form=form, title='Reset request')


@authorization.route("/request_token/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('tasks.scheduled_tasks'))

    user = User.verify_token(token)
    if user is None:
        flash('This is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been updated, {}! Please login.'.format(user.username))
        return redirect(url_for('.login'))

    return render_template("reset_token.html", form=form, title='Reset password')
