from models import Course, db
from sqlalchemy import exc


def get_courses():
    courses = Course.query.all()
    return courses

def get_course(course_id):
    course = Course.query.get(course_id)
    return course
def course_exists(course_name, course_code):
    exist = Course.query.filter((Course.course_name == course_name) | (Course.course_code == course_code)).first()
    return exist

def search_course(search_data):
    course = Course.query.filter((Course.course_name == search_data) | (Course.course_code == search_data)).first()
    
    if not course:
        return None
    return course

def add_course(course_name, added_by, course_code):
    try:
        new_course = Course(
            course_name = course_name,
            course_code = course_code,
            added_by = added_by
        )
        db.session.add(new_course)
        db.session.commit()
        return True
    except exc.IntegrityError:
        db.session.rollback()
        return False
    
def update_course(course_name, course_id, course_code):
    try:
        course = Course.query.get(course_id)
        if not course:
            return False
        course.course_name = course_name
        course.course_code = course_code
        db.session.commit()
        return True
    except exc.IntegrityError:
        db.session.rollback()
        return False

def delete_course(course_id):
    try:
        course = Course.query.get(course_id)
        if not course:
            return False
        db.session.delete(course)
        db.session.commit()
        return True
    except exc.IntegrityError:
        db.session.rollback()
        return False