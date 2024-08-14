# STUDENT MANAGEMENT APP
#### Video Link:  https://youtu.be/Pl3YU2fG89Y

### Project Description:


STUDENT MANAGEMENT APP is a comprehensive web application designed to streamline the management of courses and users within an educational institution. Built with Flask and SQLAlchemy, this application provides a user-friendly interface for both students and administrators, allowing for efficient handling of course registrations, user profiles, and administrative tasks.

### Features

#### User Authentication
- Secure login and signup processes with password hashing.
- Role-based access control (Student and Admin roles).

#### Student Dashboard and Profile
- View registered courses and personal profile information.
- Update profile details including name, surname, username, email, and password.

#### Course Management
- Students can register and unregister for courses.
- Admins can add, delete, and search for courses.

#### User Management (Admin)
- Admins can add, search, and delete users.
- Default password assignment for new users.

#### Additional Features
- Flash messages for user feedback on actions (e.g., successful registration, errors).
- Persistent login sessions with Flask-Login.
- Database migrations handled by Flask-Migrate.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/coursehub.git
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database:**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. **Run the application:**
   ```bash
   flask run
   ```

### Usage

- **Login:** Navigate to `/login` and use your credentials to log in.
- **Signup:** Register a new account at `/signup`.
- **Dashboard:** Access the dashboard at `/` to view registered courses and profile details.
-**Peofile:** Acces the profile details`/profile` to view profile and update profile details
- **Courses:** Manage your courses at `/courses` (students) and `/courses-admin` (admins).
- **Users:** Admins can manage users at `/users-admin`.

### Technologies Used

- **Flask:** Web framework for Python.
- **SQLAlchemy:** ORM for database interactions.
- **Flask-Login:** User session management.
- **Flask-Migrate:** Database migration handling.
- **SQLite:** Database backend.

### Contributing

We welcome contributions! Please submit a pull request or open an issue to discuss potential changes.

### License

This project is licensed under the MIT License.


#This Readme was wriring with the help of AI, some content of readme is written by AI