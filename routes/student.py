from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import Leave
from forms import LeaveApplyForm

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
@login_required
def dashboard():
    all_leaves = Leave.query.filter_by(user_id=current_user.id).order_by(Leave.created_at.desc()).all()
    approved = sum(1 for l in all_leaves if l.status == 'Approved')
    pending = sum(1 for l in all_leaves if l.status == 'Pending')
    rejected = sum(1 for l in all_leaves if l.status == 'Rejected')
    
    return render_template('dashboards/student.html', title='My Dashboard',
                           leaves=all_leaves, total=len(all_leaves),
                           approved=approved, pending=pending, rejected=rejected)

@student_bp.route('/leave/apply', methods=['GET', 'POST'])
@login_required
def apply_leave():
    form = LeaveApplyForm()
    if form.validate_on_submit():
        # Handle file upload if any later
        leave = Leave(user_id=current_user.id, leave_type=form.leave_type.data,
                      from_date=form.from_date.data, to_date=form.to_date.data,
                      from_time=form.from_time.data, to_time=form.to_time.data,
                      reason=form.reason.data)
        db.session.add(leave)
        db.session.commit()
        flash('Your leave request has been submitted.', 'success')
        return redirect(url_for('student.dashboard'))
    return render_template('leave/apply.html', title='Apply for Leave', form=form)
