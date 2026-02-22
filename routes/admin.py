from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db, bcrypt
from models import User, Leave, AuditLog
from routes.auth import admin_required
from forms import AdminUserForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    active_users = User.query.filter_by(status='Active').count()
    pending_users = User.query.filter_by(status='Pending').count()
    leaves_today = Leave.query.filter_by(status='Approved', from_date=db.func.current_date()).count() # Approximation
    pending_leaves = Leave.query.filter_by(status='Pending').count()
    
    users = User.query.order_by(User.created_at.desc()).limit(10).all()
    recent_leaves = Leave.query.order_by(Leave.created_at.desc()).limit(10).all()
    
    return render_template('dashboards/admin.html', title='Admin Dashboard',
                           total_users=total_users, active_users=active_users,
                           pending_users=pending_users, leaves_today=leaves_today,
                           pending_leaves=pending_leaves, users=users, recent_leaves=recent_leaves)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    all_users = User.query.all()
    return render_template('admin/users.html', title='Manage Users', users=all_users)

@admin_bp.route('/user/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = AdminUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password_hash=hashed_password,
                    role=form.role.data, department=form.department.data, stream=form.stream.data, status='Active', created_by=current_user.id)
        db.session.add(user)
        db.session.commit()
        
        log = AuditLog(action=f"Added User {user.email}", actor_id=current_user.id, target_id=user.id)
        db.session.add(log)
        db.session.commit()
        
        flash('User has been created and activated!', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/add_user.html', title='Add User', form=form)

@admin_bp.route('/user/<int:user_id>/activate')
@login_required
@admin_required
def activate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.status = 'Active'
    db.session.commit()
    flash(f'{user.name} has been activated.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/user/<int:user_id>/deactivate')
@login_required
@admin_required
def deactivate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.status = 'Inactive'
    db.session.commit()
    flash(f'{user.name} has been deactivated.', 'warning')
    return redirect(url_for('admin.users'))

@admin_bp.route('/leaves')
@login_required
@admin_required
def all_leaves():
    leaves = Leave.query.order_by(Leave.created_at.desc()).all()
    return render_template('admin/leaves.html', title='All Leaves', leaves=leaves)

@admin_bp.route('/leave/<int:leave_id>/override/<status>')
@login_required
@admin_required
def override_leave(leave_id, status):
    leave = Leave.query.get_or_404(leave_id)
    if status in ['Approved', 'Rejected']:
        leave.status = status
        leave.approved_by = current_user.id
        leave.remarks = "Overridden by Admin"
        db.session.commit()
        
        log = AuditLog(action=f"Overrode leave {leave.id} to {status}", actor_id=current_user.id, target_id=leave.id)
        db.session.add(log)
        db.session.commit()
        flash(f'Leave {status}.', 'success')
    return redirect(url_for('admin.all_leaves'))

@admin_bp.route('/user/<int:user_id>/view')
@login_required
@admin_required
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('profile/view_user.html', title='User Details', user=user)
