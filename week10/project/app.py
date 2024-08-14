import os
import re
from flask import Flask, request, render_template, redirect, url_for, jsonify, flash
from sqlalchemy import exc
import hashlib
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import secrets
from flask_migrate import Migrate

# models and controllers 
from models import User, Course, Registered, db
from controllers.users import add_user, get_user, get_users, update_user, delete_user, get_user_by_username
from controllers.course import get_courses, get_course, add_course, update_course, delete_course, course_exists, search_course
from controllers.registered import register, unregister, get_registered_courses


# initilizing flask app
file_path = os.path.abspath(os.getcwd())+ r"\database.db"
app = Flask(__name__, template_folder = 'templates', static_folder = 'static')
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)



# flask login 
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# Global varibales 
DEFAULTPASSWORD = 'student123456'

# login manager
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
    # return User.query.get(int(user_id))


# index route
@app.route('/', methods = ['GET', 'POST'])
@login_required
def index():
    if current_user.is_authenticated:
        user = get_user(current_user.id)
        registered = get_registered_courses(current_user.id)
        if user:
            role = user.role
        else:
            role = None
    else:
        role = None 

    if role is None:
        return redirect(url_for('login'))
    
    return render_template('index.html', role=role, user=user, id = int(user.id), courses = registered)

# profile route
@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    if current_user.is_authenticated:
        user = get_user(current_user.id)
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['surname']
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        if user.password == hashed_password:
            update_user(current_user.id, username, hashed_password, email, role, name, last_name)
            return redirect('/profile')
    return render_template('profile.html', role = user.role , user=user, id = int(user.id))

# student courses route
@app.route('/courses', methods = ['GET', 'POST'])
@login_required
def courses():
    if current_user.is_authenticated:
        user = get_user(current_user.id)
        
    if not user:
        return "User not found", 404
    
    courses  = get_courses()
    registered = get_registered_courses(current_user.id)
    if request.method == 'POST':
        action = request.form['action']
        form_type = request.form['formType']
        if form_type == 'registerCourse' and action == 'add':
            course_id = request.form['course_id_add']
            user_id = current_user.id
            
            if not course_id or not user_id:
                flash("Unable to Course Course. Please try again.")
                return redirect(url_for('courses'))
            elif register(course_id, user_id):
                flash("User registered successfully!")
                return redirect(url_for('courses'))
        elif form_type == 'unregisterCourse' and action == 'delete':
            course_id = request.form['course_id_delete']
            user_id = current_user.id

            if not course_id or not user_id:
                flash("User unregistered successfully!")
                return redirect(url_for('courses'))
            elif unregister(course_id, user_id):
                flash("User successfully registered from the course!")
                return redirect(url_for('courses'))
        
    return render_template('courses.html', role = user.role , user = user, courses = courses, currentCourses = registered, id = int(user.id))

# Admin courses management route
@app.route('/courses-admin', methods = ['GET', 'POST'])
@login_required
def coursesmg():
    
    if current_user.is_authenticated:
        user = get_user(current_user.id)
    if not user:
        return "User not found", 404
    if request.method == 'POST':
        action = request.form['action']
        form_type = request.form['formType']
        if form_type == 'addForm':
            if action == 'add':
                # get data from form 
                course_name = request.form['CourseName']
                course_code = request.form['CourseCode']
                
                if not course_code or not course_name:
                    flash("Unable to add new course. Please fill all fields and try again.")
                    return redirect(url_for('coursesmg'))
                
                # convert to upper
                course_name = course_name.upper()
                course_code = course_code.upper()
                
                # current user id
                added_by = user.id
                
                # check existing courses from database
                if course_exists(course_name, course_code):
                    flash('The Course code or name already exists.')
                    return redirect(url_for('coursesmg'))
                if add_course(course_name, added_by, course_code):
                    flash("New course added successfully!")
                    return redirect(url_for('coursesmg'))
        if form_type == 'deleteForm':
            if action == 'search':
                search_value = request.form['searchCourse']
                search = search_course(search_value.upper())
                if search is None:
                    flash("The course doen't exist.")
                    return redirect(url_for('coursesmg'))
                return render_template('coursesmg.html',role = user.role , user=user, search_result = search)
            elif action == 'delete':
                course_id = request.form['course_id']
                if delete_course(course_id):
                    flash("Course deleted successfully!")
                    return redirect(url_for('coursesmg'))
                else:
                    flash("Unable to delete Course. Please try again.")
                    return redirect(url_for('coursesmg'))
                    
    return render_template('coursesmg.html', role = user.role , user=user)

# Admin users managemnet route
@app.route('/users-admin', methods = ['GET', 'POST'])
@login_required
def usermg():
    if current_user.is_authenticated:
        user = get_user(current_user.id)
    if not user:
        return "User not found", 404
    usertype = ['student', 'admin']
    
    if request.method == 'POST':
        action = request.form['action']
        form_type = request.form['formType']
        if form_type == 'addUser' and action == 'add':
            name = request.form['name']
            last_name = request.form['last_name']
            username = request.form['username']
            email = request.form['email']
            role = request.form['user_type']
            password = DEFAULTPASSWORD
            
            # check if there are empty fileds
            if not name or not last_name or not username or not email or not role or not password:
                flash("Unable to register new user. Please fill all fields and try again.")
                return redirect(url_for('usermg'))
            
            # hash the default password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            if add_user(name, last_name, username, email, role, hashed_password):
                flash("User registered successfully!")
                return redirect(url_for('usermg'))
            else:
                flash("Unable to register user. Please try again.")
                return redirect(url_for('usermg'))
        if form_type == 'deleteForm' and action == 'search':
            search_value = request.form['userno']
            search_result = get_user_by_username(search_value)
            if not search_result:
                flash("The user doen't exist.")
                return redirect(url_for('usermg'))
            return render_template('usersmg.html', role = user.role , user=user, user_type = usertype, search_result = search_result) 
        elif form_type == 'deleteForm' and action == 'delete':
            user_id = request.form['user_id']
            if delete_user(user_id):
                flash("User deleted successfully!")
                return redirect(url_for('usermg'))
            else:
                flash("Unable to delete User. Please try again.")
                return redirect(url_for('usermg'))
        
    return render_template('usersmg.html', role = user.role , user=user, user_type = usertype, id = int(user.id))

    
#  Log in route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        username = username.lower()
        user = get_user_by_username(username)

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if user and user.password == hashed_password:
            login_user(user, remember=True)
            flash('Login successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

# New registration route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form['name']
        last_name = request.form['surname']
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']
        confirmation = request.form['confirmation']
        
        name = name.capitalize()
        last_name = last_name.capitalize()
        username = username.lower()
        email = email.lower()
        if not name or not last_name or not username or not email or not role or not password or not confirmation:
            flash("Unable to register user. Please fill all fields and try again.")
            return redirect(url_for('signup'))
        
        if password != confirmation:
            flash("Password and confirmation didn't match")
            return redirect(url_for('signup'))
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        if add_user(name, last_name, username, email, role, hashed_password):
            flash("User registered successfully!")
            return redirect(url_for('login'))
        else:
            flash("Unable to register user. Please try again.")
            return redirect(url_for('signup'))
    else:
        return render_template("signup.html")


# Log out route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug = True)