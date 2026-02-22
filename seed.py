import os
from app import create_app, db, bcrypt
from models import User

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Create all tables (SQLite will automatically create the leave_management.db file)
        db.create_all()
        print("Database tables created.")
        
        # Seed Admin
        admin = User.query.filter_by(email='admin@leaveportal.com').first()
        hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')
        
        if not admin:
            new_admin = User(
                name='System Admin', email='admin@leaveportal.com', password_hash=hashed_pw,
                role='Admin', status='Active', department='Administration'
            )
            db.session.add(new_admin)
            print("Default admin created: admin@leaveportal.com / password123")
        
        # Seed Manager
        manager = User.query.filter_by(email='manager@leaveportal.com').first()
        if not manager:
            new_manager = User(
                name='Jane Manager', email='manager@leaveportal.com', password_hash=hashed_pw,
                role='Manager', status='Active', department='IT'
            )
            db.session.add(new_manager)
            print("Default manager created: manager@leaveportal.com / password123")

        # Seed Faculty
        faculty = User.query.filter_by(email='faculty@leaveportal.com').first()
        if not faculty:
            new_faculty = User(
                name='Dr. Smith Faculty', email='faculty@leaveportal.com', password_hash=hashed_pw,
                role='Faculty', status='Active', department='Computer Science', stream='B.Tech'
            )
            db.session.add(new_faculty)
            print("Default faculty created: faculty@leaveportal.com / password123")
            
        db.session.commit()
            
        # Seed Employee
        employee = User.query.filter_by(email='employee@leaveportal.com').first()
        m_user = User.query.filter_by(email='manager@leaveportal.com').first()
        if not employee:
            new_employee = User(
                name='John Employee', email='employee@leaveportal.com', password_hash=hashed_pw,
                role='Employee', status='Active', department='IT', manager_id=m_user.id if m_user else None
            )
            db.session.add(new_employee)
            print("Default employee created: employee@leaveportal.com / password123")

        # Seed Student
        student = User.query.filter_by(email='student@leaveportal.com').first()
        f_user = User.query.filter_by(email='faculty@leaveportal.com').first()
        if not student:
            new_student = User(
                name='Alice Student', email='student@leaveportal.com', password_hash=hashed_pw,
                role='Student', status='Active', department='Computer Science', stream='B.Tech',
                manager_id=f_user.id if f_user else None
            )
            db.session.add(new_student)
            print("Default student created: student@leaveportal.com / password123")

        db.session.commit()
        print("Database seeded successfully with all roles!")
