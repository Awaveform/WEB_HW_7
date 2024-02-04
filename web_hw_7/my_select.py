from sqlalchemy import func, desc
from sqlalchemy.orm import aliased

from web_hw_7 import Group, Student, Teacher, Subject, Grade
from web_hw_7 import Session


# Function to find 5 students with the highest average grade across all subjects
def select_1():
    with Session() as session:
        result = (
            session.query(
                func.concat(Student.first_name, ' ', Student.last_name).label('fullname'),
                func.round(func.avg(Grade.grade), 2).label('avg_grade')
            )
            .select_from(Grade)
            .join(Student)
            .group_by(Student.first_name)
            .group_by(Student.last_name)
            .order_by(desc('avg_grade'))
            .limit(5)
            .all()
        )
        return result


def select_2():
    with Session() as session:
        subquery = (
            session.query(Subject.id)
            .order_by(func.random())
            .limit(1)
            .scalar_subquery()
        )

        result = (
            session.query(Student.first_name, Student.last_name,
                           func.round(func.avg(Grade.grade), 2).label('average_grade'),
                           Subject.subject_name.label('selected_subject'))
            .join(Grade, Student.id == Grade.student_id)
            .join(Subject, Grade.subject_id == Subject.id)
            .filter(Grade.subject_id == subquery)
            .group_by(Student.first_name, Student.last_name, Subject.subject_name)
            .order_by(desc('average_grade'))
            .limit(1)
            .first()
        )

        return result


# Function to find the average grade in groups for a specific subject
def select_3():
    with Session() as session:
        subquery = (
            session.query(Subject.id)
            .order_by(func.random())
            .limit(1)
            .scalar_subquery()
        )

        result = (
            session.query(Group.group_name,
                           func.round(func.avg(Grade.grade), 2).label('average_grade'),
                           Subject.subject_name.label('selected_subject'))
            .join(Student, Group.id == Student.group_id)
            .join(Grade, Student.id == Grade.student_id)
            .join(Subject, Grade.subject_id == Subject.id)
            .filter(Grade.subject_id == subquery)
            .group_by(Group.group_name, Subject.subject_name)
            .all()
        )

        return result


# Function to find the average grade across all subjects
def select_4():
    with Session() as session:
        result = (
            session.query(
                func.round(func.avg(Grade.grade), 2).label('average_grade'))
            .first()
        )

        return result.average_grade if result else None


# Function to find the courses taught by a specific teacher
def select_5():
    with Session() as session:
        subquery = (
            session.query(Teacher.id)
            .order_by(func.random())
            .limit(1)
            .scalar_subquery()
        )

        teacher_alias = aliased(Teacher)
        subject_alias = aliased(Subject)

        result = (
            session.query(teacher_alias.teacher_name, subject_alias.subject_name)
            .join(subject_alias, teacher_alias.id == subject_alias.teacher_id)
            .filter(teacher_alias.id == subquery)
            .distinct()
            .all()
        )

        return result


# Function to find the list of students in a specific group
def select_6():
    with Session() as session:
        subquery = (
            session.query(Group.id)
            .order_by(func.random())
            .limit(1)
            .scalar_subquery()
        )

        student_alias = aliased(Student)
        group_alias = aliased(Group)

        result = (
            session.query(student_alias.first_name, student_alias.last_name, group_alias.group_name)
            .join(group_alias, student_alias.group_id == group_alias.id)
            .filter(student_alias.group_id == subquery)
            .all()
        )

        return result


# Function to find the grades of students in a specific group for a specific subject
def select_7():
    with Session() as session:
        group_subquery = (
            session.query(Group.id)
            .order_by(func.random())
            .limit(1)
            .scalar_subquery()
        )

        subject_subquery = (
            session.query(Subject.id)
            .order_by(func.random())
            .limit(1)
            .scalar_subquery()
        )

        result = (
            session.query(Student.first_name, Student.last_name, Grade.grade, Group.group_name, Subject.subject_name)
            .join(Group, Student.group_id == Group.id)
            .join(Grade, Student.id == Grade.student_id)
            .join(Subject, Grade.subject_id == Subject.id)
            .filter(Student.group_id == group_subquery, Grade.subject_id == subject_subquery)
            .all()
        )

        return result


# Function to find the average grade given by a specific teacher for their subjects
def select_8():
    with Session() as session:
        subquery = (
            session.query(Teacher.id)
            .join(Subject, Teacher.id == Subject.teacher_id)
            .join(Grade, Subject.id == Grade.subject_id)
            .group_by(Teacher.id)
            .order_by(func.random())
            .limit(1)
            .scalar_subquery()
        )

        result = (
            session.query(Teacher.teacher_name, func.avg(Grade.grade).label('average_grade'))
            .join(Subject, Teacher.id == Subject.teacher_id)
            .join(Grade, Subject.id == Grade.subject_id)
            .filter(Teacher.id == subquery)
            .group_by(Teacher.id)
            .all()
        )

        return result


# Function to find the list of courses attended by a specific student
def select_9():
    with Session() as session:
        subquery = (
            session.query(Student.id)
            .order_by(func.random())
            .limit(1)
            .scalar_subquery()
        )

        result = (
            session.query(Student.first_name, Student.last_name, Subject.subject_name)
            .join(Grade, Student.id == Grade.student_id)
            .join(Subject, Grade.subject_id == Subject.id)
            .filter(Student.id == subquery)
            .distinct()
            .all()
        )

        return result


# Function to find the list of courses taught to a specific student by a specific teacher
def select_10():
    with Session() as session:
        student_subquery = (
            session.query(Student.id)
            .order_by(func.random())
            .limit(1)
            .scalar_subquery()
        )

        teacher_subquery = (
            session.query(Teacher.id)
            .order_by(func.random())
            .limit(1)
            .scalar_subquery()
        )

        result = (
            session.query(Subject.subject_name, Student.first_name, Student.last_name, Teacher.teacher_name)
            .join(Grade, Subject.id == Grade.subject_id)
            .join(Student, Grade.student_id == Student.id)
            .join(Teacher, Subject.teacher_id == Teacher.id)
            .filter(Student.id == student_subquery, Teacher.id == teacher_subquery)
            .distinct()
            .all()
        )

        return result



# Test the functions
if __name__ == "__main__":
    print("Select 1:", select_1())
    print("Select 2:", select_2())
    print("Select 3:", select_3())
    print("Select 4:", select_4())
    print("Select 5:", select_5())
    print("Select 6:", select_6())
    print("Select 7:", select_7())
    print("Select 8:", select_8())
    print("Select 9:", select_9())
    print("Select 10:", select_10())
