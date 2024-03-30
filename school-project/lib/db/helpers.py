from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Attendance, User
from datetime import datetime

# Create an SQLite database engine
engine = create_engine('sqlite:///attendance_tracker.db', echo=True)

# Create a session
Session = sessionmaker(bind=engine)
db_session = Session()

def associate_student_with_teacher(student, teacher):
    """Associate a student with a teacher."""
    student.teachers.append(teacher)
    db_session.commit()

def dissociate_student_from_teacher(student):
    """Remove the link between a student and his/her teacher."""
    student.teachers = []
    db_session.commit()

# Create an SQLite database engine
engine = create_engine('sqlite:///attendance_tracker.db', echo=True)

# Create a session
Session = sessionmaker(bind=engine)
db_session = Session()

def mark_attendance(user_id, date, status):
    """Mark attendance for a user."""
    user = db_session.query(User).filter_by(id=user_id).first()
    if user:
        if not isinstance(date, datetime):
            date = datetime.fromisoformat(date)  # Assuming date is in ISO format
        attendance = Attendance(user_id=user_id, date=date, status=status)
        db_session.add(attendance)
        db_session.commit()
        print(f"{user.role.capitalize()} attendance marked successfully.")
    else:
        print("User not found.")

def update_attendance_status(user_id, new_status):
    """Update attendance status for a user."""
    user = db_session.query(User).filter_by(id=user_id).first()
    if user:
        mark_attendance(user_id, datetime.now(), new_status)
        print(f"Attendance status has been updated successfully for user ID {user.id}")
    else:
        print("User not found.")

def view_attendance(user_id):
    """View attendance records for a user."""
    user = db_session.query(User).filter_by(id=user_id).first()
    if user:
        attendance_records = user.attendance
        for record in attendance_records:
            print(f"Date: {record.date}, Status: {record.status}")
    else:
        print("User not found.")

def generate_attendance_report(user_id):
    """Generate attendance report for a user."""
    user = db_session.query(User).filter_by(id=user_id).first()
    if user:
        attendance_records = user.attendance
        present_count = sum(1 for record in attendance_records if record.status == 'Present')
        total_days = len(attendance_records)
        attendance_percentage = (present_count / total_days) * 100 if total_days > 0 else 0
        print(f"{user.role.capitalize()} ID: {user_id}")
        print(f"Total Days: {total_days}")
        print(f"Present Days: {present_count}")
        print(f"Attendance Percentage: {attendance_percentage:.2f}%")
    else:
        print("User not found.")
