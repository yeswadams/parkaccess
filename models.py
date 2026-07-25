"""
Database models for the mini project.

Three tables:
    Student     -- a learner
    Course      -- a course they can take
    Enrollment  -- the join table linking Student <-> Course
                   (many-to-many)
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy # type: ignore[import]

db = SQLAlchemy() # creates the db sqlalchemy instance 


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)
    adm_number = db.Column(db.Integer, unique=True, nullable=True)

    # backref "student" is created automatically on Enrollment
    # via the relationship defined below.

    def __repr__(self):
        return f"<Student {self.name}>"


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    credits = db.Column(db.Integer, default=3)

    def __repr__(self):
        return f"<Course {self.title}>"


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    enrolled_on = db.Column(db.DateTime, default=datetime.utcnow)
    # binding the relationship
    student = db.relationship("Student", backref="enrollments")
    course = db.relationship("Course", backref="enrollments")

    def __repr__(self):
        return f"<Enrollment student={self.student_id} course={self.course_id}>"
