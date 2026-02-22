from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Student') # Admin, Manager, Student
    status = db.Column(db.String(20), nullable=False, default='Pending') # Pending, Active, Inactive
    
    # Organizational Details
    department = db.Column(db.String(100))
    stream = db.Column(db.String(100))
    batch = db.Column(db.String(50))
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Profile Details
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    gender = db.Column(db.String(10))
    dob = db.Column(db.Date)
    emergency_contact = db.Column(db.String(20))
    profile_photo = db.Column(db.String(255), default='default.jpg')
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    manager = db.relationship('User', remote_side=[id], foreign_keys=[manager_id], backref='team_members')
    creator = db.relationship('User', remote_side=[id], foreign_keys=[created_by], backref='created_users')
    leaves = db.relationship('Leave', backref='applicant', lazy=True, foreign_keys='Leave.user_id')

    def __repr__(self):
        return f'<User {self.name} - {self.role}>'

class Leave(db.Model):
    __tablename__ = 'leaves'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False) # Casual, Sick, Permission, etc.
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    from_time = db.Column(db.Time, nullable=True) # Used for short permissions
    to_time = db.Column(db.Time, nullable=True)
    reason = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(255), nullable=True)
    
    status = db.Column(db.String(20), nullable=False, default='Pending') # Pending, Approved, Rejected
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    approver = db.relationship('User', foreign_keys=[approved_by], backref='approved_leaves')

    def __repr__(self):
        return f'<Leave {self.leave_type} for User {self.user_id}>'

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    target_id = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    actor = db.relationship('User', foreign_keys=[actor_id])
    
    def __repr__(self):
        return f'<AuditLog {self.action} by User {self.actor_id}>'
