"""
Mini Project: Student-Course Database
--------------------------------------
Entry point for the Flask app. Run this file directly to start a dev
server.
"""

from flask import Flask, jsonify  # type: ignore[import]
from flask_migrate import Migrate  # type: ignore[import] 
from models import db, Student, Course, Enrollment

app = Flask(__name__)

# ---- Configuration (.env - reference from .env )----
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ---- Bind SQLAlchemy to this app ----
db.init_app(app)
migrate = Migrate(app, db)


# ---- A couple of simple routes so you can see the data in a browser ----

@app.route("/")
def index():
    return {
        "message": "Student-Course mini project is running.",
        "try": ["/students", "/courses", "/students/1/courses"],
    }


@app.route("/students")
def list_students():
    students = Student.query.all() #fetching records from the db
    return jsonify([
        {"id": s.id, "name": s.name, "email": s.email}
        for s in students
    ])


@app.route("/courses")
def list_courses():
    courses = Course.query.all() 
    return jsonify([
        {"id": c.id, "title": c.title, "credits": c.credits}
        for c in courses
    ])


@app.route("/students/<int:student_id>/courses")
def student_courses(student_id):
    student = Student.query.get_or_404(student_id) # fetching a single student , return 404 error if not found
    courses = [enrollment.course.title for enrollment in student.enrollments]
    return jsonify({"student": student.name, "courses": courses})


if __name__ == "__main__":
    # Make sure tables exist before serving requests.
    # (In a real project you'd normally run seed.py once instead.)
    with app.app_context():
        db.create_all() # creates the table if it does not exist 
    app.run(debug=True) # debug logs if app crashes
