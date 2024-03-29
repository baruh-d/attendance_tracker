from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import association_table, Attendance, Teacher, Student, User
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

def mark_student_attendance(student_id, date, status):
    """Mark attendance for a student."""
    student = db_session.query(Student).filter_by(id=student_id).first()
    if student:
        attendance = Attendance(person_id=student_id, person_type='student', date=date, status=status)
        db_session.add(attendance)
        db_session.commit()
        print("Student attendance marked successfully.")
    else:
        print("Student not found.")

def mark_teacher_attendance(teacher_id, date, status):
    """Mark attendance for a teacher."""
    teacher = db_session.query(Teacher).filter_by(id=teacher_id).first()
    if teacher:
        attendance = Attendance(person_id=teacher_id, person_type='teacher', date=date, status=status)
        db_session.add(attendance)
        db_session.commit()
        print("Teacher attendance marked successfully.")
    else:
        print("Teacher not found.")

def update_attendance_status(user_id, new_status):
    """Update attendance status for a user."""
    user = db_session.query(User).filter_by(id=user_id).first()
    if user:
        if isinstance(user, Teacher):
            mark_teacher_attendance(user_id, datetime.now(), new_status)
        elif isinstance(user, Student):
            mark_student_attendance(user_id, datetime.now(), new_status)
        print(f"Attendance status has been updated successfully for user ID {user.id}")
    else:
        print("User not found.")

def view_student_attendance(student_id):
    """View attendance records for a student."""
    student = db_session.query(Student).filter_by(id=student_id).first()
    if student:
        attendance_records = student.attendance
        for record in attendance_records:
            print(f"Date: {record.date}, Status: {record.status}")
    else:
        print("Student not found.")

def view_teacher_attendance(teacher_id):
    """View attendance records for a teacher."""
    teacher = db_session.query(Teacher).filter_by(id=teacher_id).first()
    if teacher:
        attendance_records = teacher.attendance
        for record in attendance_records:
            print(f"Date: {record.date}, Status: {record.status}")
    else:
        print("Teacher not found.")

def generate_student_attendance_report(student_id):
    """Generate attendance report for a student."""
    student = db_session.query(Student).filter_by(id=student_id).first()
    if student:
        attendance_records = student.attendance
        present_count = sum(1 for record in attendance_records if record.status == 'Present')
        total_days = len(attendance_records)
        attendance_percentage = (present_count / total_days) * 100 if total_days > 0 else 0
        print(f"Student ID: {student_id}")
        print(f"Total Days: {total_days}")
        print(f"Present Days: {present_count}")
        print(f"Attendance Percentage: {attendance_percentage:.2f}%")
    else:
        print("Student not found.")

def generate_teacher_attendance_report(teacher_id):
    """Generate attendance report for a teacher."""
    teacher = db_session.query(Teacher).filter_by(id=teacher_id).first()
    if teacher:
        attendance_records = teacher.attendance
        present_count = sum(1 for record in attendance_records if record.status == 'Present')
        total_days = len(attendance_records)
        attendance_percentage = (present_count / total_days) * 100 if total_days > 0 else 0
        print(f"Teacher ID: {teacher_id}")
        print(f"Total Days: {total_days}")
        print(f"Present Days: {present_count}")
        print(f"Attendance Percentage: {attendance_percentage:.2f}%")
    else:
        print("Teacher not found.")
