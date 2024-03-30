from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime
from faker import Faker

# Create a declarative base
Base = declarative_base()

# Define association table for many-to-many relationship between students and teachers
association_table = Table('association', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('teacher_id', Integer, ForeignKey('teachers.id'))
)

# Define User class representing both students and teachers
class User(Base):
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(Enum('student', 'teacher'))  # 'teacher' or 'student'

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }

# Define Teacher class
class Teacher(User):
    __tablename__ = 'teachers'

    id = Column(String, ForeignKey('users.id'), primary_key=True)
    name = Column(String)
    email = Column(String)
    students = relationship('Student', secondary=association_table, back_populates='teachers')

    __mapper_args__ = {
        'polymorphic_identity': 'teacher'
    }

# Define Student class
class Student(User):
    __tablename__ = 'students'

    id = Column(String, ForeignKey('users.id'), primary_key=True)
    name = Column(String)
    roll_number = Column(Integer)
    teachers = relationship('Teacher', secondary=association_table, back_populates='students')

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

# Define Attendance class to track attendance records
class Attendance(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))  # References either student or teacher
    date = Column(DateTime, default=datetime.now())  # Date of the attendance record
    status = Column(String)  # Attendance status: Present, Absent, Late, etc.

# Main code execution
if __name__ == "__main__":
    # Create an SQLite database engine
    engine = create_engine('sqlite:///attendance_tracker.db', echo=True)
    
    # Create tables in the database based on the defined models
    Base.metadata.create_all(engine)

    # Create a sessionmaker bound to the engine
    Session = sessionmaker(bind=engine)
    db_session = Session()
    
