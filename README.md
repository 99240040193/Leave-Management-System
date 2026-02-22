# Leave Portal

A complete company-style Leave and Permission Management Web Application built with Python, Flask, and SQLite.

## Features

- **Role-Based Access Control**: Three distinct roles - Admin, Manager/Faculty, and Student/Employee.
- **Admin Dashboard**: System-wide statistics, global user management, leave request overrides, and organization oversight.
- **Manager/Faculty Dashboard**: Team-specific leave tracking, adding new team members, and approving/rejecting leave requests.
- **Student/Employee Portal**: Personal dashboard, leave application form, and leave history log.
- **User Profiles**: Manage personal details, emergency contacts, and profile picture (via UI Avatars fallback).
- **Responsive UI**: Built with Bootstrap 5, featuring a sidebar layout, glassmorphism cards, and modern aesthetics.

## Prerequisites

- Python 3.8+
- Active virtual environment

## Installation & Setup

1. **Clone the repository** (if you haven't already) and navigate to the project folder:
   ```bash
   cd Leave_platform
   ```

2. **Activate the Virtual Environment**:
   - On Windows (PowerShell):
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - On Windows (Command Prompt):
     ```cmd
     .\.venv\Scripts\activate.bat
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**:
   The application uses an SQLite database by default (`leave_portal.db`). Run the seed script to create the necessary tables and generate the default Admin user.
   ```bash
   python seed.py
   ```

5. **Run the Application**:
   Start the Flask development server:
   ```bash
   python run.py
   ```

6. **Access the Portal**:
   Open your web browser and go to: `http://127.0.0.1:5000`

## Predefined Login Credentials for Evaluation

When you run `python seed.py`, the following accounts are automatically created for quick evaluation:

| Role | Email | Password |
|---|---|---|
| **Admin** | `admin@leaveportal.com` | `password123` |
| **Manager** | `manager@leaveportal.com` | `password123` |
| **Faculty** | `faculty@leaveportal.com` | `password123` |
| **Employee** | `employee@leaveportal.com` | `password123` |
| **Student** | `student@leaveportal.com` | `password123` |

## Initial Verification & Testing

To verify the system is working correctly, you can use the predefined credentials above to explore each portal:

1. **Log in as Admin**
   - **Email:** `admin@leaveportal.com`
   - **Password:** `password123`
   - *Action:* Explore the Admin dashboard, "Manage Users", and "System Leaves" menus.

2. **Log in as Manager / Faculty**
   - **Email:** `manager@leaveportal.com` (or `faculty@leaveportal.com`)
   - **Password:** `password123`
   - *Action:* Go to "My Team". You will see pre-assigned team members. Click "Add Team Member" or view their robust profiles.

3. **Log in as Student / Employee**
   - **Email:** `student@leaveportal.com` (or `employee@leaveportal.com`)
   - **Password:** `password123`
   - *Action:* Go to "Apply Leave", fill out the form, and submit a new leave request.

4. **Approve the Leave**
   - Log back in as the Manager/Faculty.
   - *Action:* Review the pending leave request on your dashboard and Approve or Reject it.

## Project Structure

- `app.py`: Flask application factory and core configurations.
- `run.py`: Entry point to run the application server.
- `config.py`: Environment variables and configuration settings.
- `models.py`: SQLAlchemy database models (`User`, `Leave`, `AuditLog`).
- `forms.py`: WTForms definitions for validation.
- `seed.py`: Database initialization and mock data generation.
- `routes/`: Modularized Flask blueprints for routing (`auth.py`, `admin.py`, `manager.py`, `student.py`, `profile.py`).
- `templates/`: Jinja2 HTML templates styled with Bootstrap 5.
- `static/`: Static assets (images, profile pictures).
