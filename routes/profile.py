from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from forms import ProfileUpdateForm

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def view_edit():
    form = ProfileUpdateForm(obj=current_user)
    if form.validate_on_submit():
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        current_user.gender = form.gender.data
        current_user.dob = form.dob.data
        current_user.emergency_contact = form.emergency_contact.data
        
        # Profile photo upload logic can be added here
        
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('profile.view_edit'))
    
    return render_template('profile/view.html', title='Complete Profile', form=form)
