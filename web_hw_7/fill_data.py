# Create a session to interact with the database
import random

from faker import Faker
from sqlalchemy.orm import sessionmaker

from web_hw_7 import engine
from web_hw_7 import Group, Student, Teacher, Subject, Grade

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()


def insert_students(session, num_students, num_groups):
    groups = session.query(Group).all()

    students = [Student(first_name=fake.name().split()[0],
                        last_name=fake.name().split()[1],
                        date_of_birth=fake.date_of_birth(),
                        group=random.choice(groups))
                for _ in range(num_students)]

    session.add_all(students)
    session.commit()


def insert_groups(session, num_groups):
    groups = [Group(group_name=fake.word()) for _ in range(num_groups)]

    session.add_all(groups)
    session.commit()


def insert_teachers(session, num_teachers):
    teachers = [Teacher(teacher_name=fake.name()) for _ in range(num_teachers)]

    session.add_all(teachers)
    session.commit()


def insert_subjects(session, num_subjects):
    teachers = session.query(Teacher).all()

    subjects = [Subject(subject_name=fake.word(), teacher=random.choice(teachers))
                for _ in range(num_subjects)]

    session.add_all(subjects)
    session.commit()


def insert_grades(session, num_students, num_subjects, max_grades_per_student):
    students = session.query(Student).all()
    subjects = session.query(Subject).all()

    grades = [Grade(student_id=random.choice(students).id,
                    subject_id=random.choice(subjects).id,
                    grade=random.randint(1, 100),
                    date_obtained=fake.date_between(start_date='-1y', end_date='today'))
              for _ in range(max_grades_per_student * num_students)]

    session.add_all(grades)
    session.commit()


def fill_data(session):
    num_students = random.randint(30, 50)
    num_groups = 3
    num_teachers = random.randint(3, 5)
    num_subjects = random.randint(5, 8)
    max_grades_per_student = 20

    insert_groups(session, num_groups)
    insert_students(session, num_students, num_groups)
    insert_teachers(session, num_teachers)
    insert_subjects(session, num_subjects)
    insert_grades(
        session, num_students, num_subjects, max_grades_per_student
    )

    print("Random data added to the database.")


if __name__ == "__main__":
    fill_data(session)
    engine.dispose()
