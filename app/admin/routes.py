from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app import db
from app.admin import bp
from app.models import User, Role, admin_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

# --- Forms ---
class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', coerce=int, validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create User')

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.role.choices = [(r.id, r.name) for r in Role.query.order_by(Role.name).all()]

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Update User')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
        self.role.choices = [(r.id, r.name) for r in Role.query.order_by(Role.name).all()]

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')

class ChangePasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change Password')


# --- Routes ---
@bp.route('/')
@login_required
@admin_required
def index():
    users = User.query.all()
    return render_template('admin/dashboard.html', users=users)

@bp.route('/user/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role_id=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User has been created!', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/add_user.html', form=form)

@bp.route('/user/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = EditUserForm(original_username=user.username, original_email=user.email)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role_id = form.role.data
        db.session.commit()
        flash('User has been updated!', 'success')
        return redirect(url_for('admin.index'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.role.data = user.role_id
    return render_template('admin/edit_user.html', form=form, user=user)

@bp.route('/user/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.is_admin():
        flash("Cannot delete an admin user.", "danger")
        return redirect(url_for('admin.index'))
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted.', 'success')
    return redirect(url_for('admin.index'))

@bp.route('/user/change-password/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def change_password(id):
    user = User.query.get_or_404(id)
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Password has been changed!', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/change_password.html', form=form, user=user) 