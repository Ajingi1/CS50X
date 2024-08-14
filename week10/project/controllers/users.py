from models import User, db
from sqlalchemy import exc

def get_users():
    users = User.query.all()
    return users

def get_user(id):
    user = User.query.get(id)
    return user

# def add_user(username, password, email, role, name, last_name):
def add_user(name, last_name, username, email, role, password):
    try:
        new_user = User(
            username = username,
            name = name,
            last_name = last_name,
            password = password,
            email = email,
            role = role
        )
        db.session.add(new_user)
        db.session.commit()
        return True
    except exc.IntegrityError:
        db.session.rollback()
        return False

def update_user(id, username, password, email, role, name, last_name):
    try:
        user = User.query.get(id)
        if not user:
            return False
        user.username = username
        user.name = name
        user.last_name = last_name
        user.password = password
        user.email = email
        user.role = role
        db.session.commit()
        return True
    except exc.IntegrityError:
        db.session.rollback()
        return False
    
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True
    except exc.IntegrityError:
        db.session.rollback()
        return False
   
def get_user_by_username(username):
    user = User.query.filter_by(username = username).first()
    if not user:
        return None
    return user

