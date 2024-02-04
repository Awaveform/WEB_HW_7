from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base


Base = declarative_base()


# Table: groups
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    group_name = Column(String(255), nullable=False)
    students = relationship('Student', backref='group')


# Table: students
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE'))


# Table: teachers
class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    teacher_name = Column(String(255), nullable=False)
    subjects = relationship('Subject', backref='teacher')


# Table: subjects
class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    subject_name = Column(String(255), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE', onupdate='CASCADE'))
    grades = relationship('Grade', backref='subject')


# Table: grades
class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE', onupdate='CASCADE'))
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE', onupdate='CASCADE'))
    grade = Column(Integer)
    date_obtained = Column(Date, nullable=False)
