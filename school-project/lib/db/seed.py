from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Teacher, Student
from random import randint
from datetime import datetime
from faker import Faker
import random
from helpers import associate_student_with_teacher, dissociate_student_from_teacher, mark_attendance

fake = Faker()

# Create an SQLite database engine
engine = create_engine('sqlite:///attendance_tracker.db', echo=True)

# Create a session
Session = sessionmaker(bind=engine)
db_session = Session()

def populate():
    teachers = []
    students = []
    student_count = 115
    teacher_start_id = '01'

    # Generate students
    for i in range(student_count):
        student_id = f's{i+1:03}'
        student_username = f'student_{student_id}'
        student_name = fake.name()
        roll_number = randint(5000, 10000)
        role = 'student'
        new_student = Student(id=student_id, username=student_username, name=student_name, roll_number=roll_number, role=role)
        students.append(new_student)

    # Generate teachers
    for i in range(7):
        teacher_id = f't{i+1:02}'
        teacher_username = f'teacher_{teacher_id}'
        teacher_name = fake.name()
        teacher_email = (teacher_name.replace(' ', '')+f"@example.com").lower()
        password = fake.password()
        role = 'teacher'
        new_teacher = Teacher(id=teacher_id, username=teacher_username, name=teacher_name, email=teacher_email, password=password, role=role)
        teachers.append(new_teacher)

    # Combine students and teachers into a single list
    all_users = students + teachers

    # Add users to the session and commit changes
    db_session.add_all(all_users)
    db_session.commit()

    # Assign teachers to students
    for student in students:
        teacher = teachers[randint(0, len(teachers)-1)]
        associate_student_with_teacher(student, teacher)
        
    print("Database populated with %s students and %s teachers." % (len(students), len(teachers)))
    db_session.commit()
    
    # Dissociate teachers from students
    for student in students:
        dissociate_student_from_teacher(student)

    # Add attendance for all users
    current_date = datetime.now()  # End date for generating random dates
    start_date = current_date.replace(year=current_date.year - 2)  # Start date for generating random dates
    attendance_statuses = ['Present', 'Absent', 'Late']  # Possible attendance statuses

    for user in all_users:
        random_date = fake.date_time_between(start_date=start_date, end_date=current_date)
        attendance_status = random.choice(attendance_statuses)
        mark_attendance(user.id, random_date, attendance_status)
    db_session.commit()

# Main code execution
if __name__ == "__main__":
    populate()  # Populate the database with data
