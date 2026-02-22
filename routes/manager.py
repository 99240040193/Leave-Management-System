from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db, bcrypt
from models import User, Leave, AuditLog
from routes.auth import manager_required
from forms import ManagerAddUserForm

manager_bp = Blueprint('manager', __name__)

@manager_bp.route('/dashboard')
@login_required
@manager_required
def dashboard():
    team_members = User.query.filter_by(manager_id=current_user.id).all()
    team_ids = [m.id for m in team_members]
    
    pending_leaves = Leave.query.filter(Leave.user_id.in_(team_ids), Leave.status == 'Pending').all()
    recent_leaves = Leave.query.filter(Leave.user_id.in_(team_ids)).order_by(Leave.created_at.desc()).limit(10).all()
    
    return render_template('dashboards/manager.html', title='Manager Dashboard',
                           team_members=team_members, pending_leaves=pending_leaves, recent_leaves=recent_leaves)

@manager_bp.route('/team')
@login_required
@manager_required
def team():
    members = User.query.filter_by(manager_id=current_user.id).all()
    return render_template('manager/team.html', title='My Team', members=members)

@manager_bp.route('/user/add', methods=['GET', 'POST'])
@login_required
@manager_required
def add_user():
    form = ManagerAddUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password_hash=hashed_password,
                    role=form.role.data, department=form.department.data, 
                    stream=form.stream.data, batch=form.batch.data,
                    manager_id=current_user.id, status='Pending', created_by=current_user.id)
        db.session.add(user)
        db.session.commit()
        
        log = AuditLog(action=f"Manager added User {user.email}", actor_id=current_user.id, target_id=user.id)
        db.session.add(log)
        db.session.commit()
        
        flash('User created. Waiting for Admin activation.', 'info')
        return redirect(url_for('manager.team'))
    return render_template('manager/add_user.html', title='Add Team Member', form=form)

@manager_bp.route('/leave/<int:leave_id>/action/<status>', methods=['GET'])
@login_required
@manager_required
def leave_action(leave_id, status):
    leave = Leave.query.get_or_404(leave_id)
    if leave.applicant.manager_id != current_user.id:
        flash('You are not authorized to approve this leave.', 'danger')
        return redirect(url_for('manager.dashboard'))
        
    if status in ['Approved', 'Rejected']:
        leave.status = status
        leave.approved_by = current_user.id
        db.session.commit()
        flash(f'Leave {status} successfully.', 'success')
    return redirect(url_for('manager.dashboard'))

@manager_bp.route('/user/<int:user_id>/view')
@login_required
@manager_required
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    # Ensure they can only view people in the system if they are a manager/faculty
    return render_template('profile/view_user.html', title='Team Member Details', user=user)
