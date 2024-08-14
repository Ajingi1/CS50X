from models import Registered, db
from sqlalchemy import exc

def register(course_id, user_id):
    try:
        new_register = Registered(
            course_id=course_id,
            user_id=user_id
        )
        db.session.add(new_register)
        db.session.commit()
        return True
    except exc.IntegrityError:
        db.session.rollback()
        return False
    
def unregister(course_id, user_id):
    try:
        registration = Registered.query.filter_by(course_id=course_id, user_id=user_id).first()
        if not registration:
            return False
        db.session.delete(registration)
        db.session.commit()
        return True
    except exc.IntegrityError:
        db.session.rollback()
        return False

def get_registered_courses(user_id):
    try:
        registrations = Registered.query.filter_by(user_id=user_id).all()
        if not registrations:
            return []
        courses = [registration.course for registration in registrations]
        return courses
    except exc.IntegrityError:
        db.session.rollback()
        return False