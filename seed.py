from app import create_app, db, bcrypt
from models import User

def seed_data():
    app = create_app()
    with app.app_context():

        db.create_all()
        print("Database tables created.")

        hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')

        # Admin
        if not User.query.filter_by(email='admin@leaveportal.com').first():
            db.session.add(User(
                name='System Admin',
                email='admin@leaveportal.com',
                password_hash=hashed_pw,
                role='Admin',
                status='Active',
                department='Administration'
            ))
            print("Admin seeded")

        # Manager
        if not User.query.filter_by(email='manager@leaveportal.com').first():
            db.session.add(User(
                name='Jane Manager',
                email='manager@leaveportal.com',
                password_hash=hashed_pw,
                role='Manager',
                status='Active',
                department='IT'
            ))
            print("Manager seeded")

        # Faculty
        if not User.query.filter_by(email='faculty@leaveportal.com').first():
            db.session.add(User(
                name='Dr. Smith Faculty',
                email='faculty@leaveportal.com',
                password_hash=hashed_pw,
                role='Faculty',
                status='Active',
                department='Computer Science',
                stream='B.Tech'
            ))
            print("Faculty seeded")

        db.session.commit()

        # Employee
        manager = User.query.filter_by(email='manager@leaveportal.com').first()
        if not User.query.filter_by(email='employee@leaveportal.com').first():
            db.session.add(User(
                name='John Employee',
                email='employee@leaveportal.com',
                password_hash=hashed_pw,
                role='Employee',
                status='Active',
                department='IT',
                manager_id=manager.id if manager else None
            ))
            print("Employee seeded")

        # Student
        faculty = User.query.filter_by(email='faculty@leaveportal.com').first()
        if not User.query.filter_by(email='student@leaveportal.com').first():
            db.session.add(User(
                name='Alice Student',
                email='student@leaveportal.com',
                password_hash=hashed_pw,
                role='Student',
                status='Active',
                department='Computer Science',
                stream='B.Tech',
                manager_id=faculty.id if faculty else None
            ))
            print("Student seeded")

        db.session.commit()
        print("✅ Database seeded successfully")
