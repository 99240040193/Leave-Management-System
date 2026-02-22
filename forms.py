from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AdminUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('Admin', 'Admin'), ('Manager', 'Manager'), ('Faculty', 'Faculty'), ('Student', 'Student'), ('Employee', 'Employee')], validators=[DataRequired()])
    department = StringField('Department')
    stream = StringField('Stream')
    submit = SubmitField('Add User')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class ManagerAddUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('Student', 'Student'), ('Employee', 'Employee')], validators=[DataRequired()])
    department = StringField('Department')
    stream = StringField('Stream')
    batch = StringField('Batch')
    submit = SubmitField('Add Team Member')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken.')

class LeaveApplyForm(FlaskForm):
    leave_type = SelectField('Leave Type', choices=[('Casual', 'Casual'), ('Sick', 'Sick'), ('Permission', 'Permission (Hourly)'), ('Other', 'Other')], validators=[DataRequired()])
    from_date = DateField('From Date', format='%Y-%m-%d', validators=[DataRequired()])
    to_date = DateField('To Date', format='%Y-%m-%d', validators=[DataRequired()])
    from_time = TimeField('From Time (For Permission)', format='%H:%M', validators=[])
    to_time = TimeField('To Time (For Permission)', format='%H:%M', validators=[])
    reason = TextAreaField('Reason for Leave', validators=[DataRequired()])
    attachment = FileField('Attachment (Optional)', validators=[FileAllowed(['jpg', 'png', 'pdf', 'doc', 'docx'])])
    submit = SubmitField('Apply Leave')

class ProfileUpdateForm(FlaskForm):
    phone = StringField('Phone', validators=[Length(max=20)])
    address = TextAreaField('Address')
    gender = SelectField('Gender', choices=[('', 'Select'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[])
    emergency_contact = StringField('Emergency Contact', validators=[Length(max=20)])
    profile_photo = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Profile')
