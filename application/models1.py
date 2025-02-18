from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin 
from flask_security import RoleMixin , SQLAlchemyUserDatastore
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define Role Model for RBAC
class Role(db.Model, RoleMixin ):
    __tablename__ = "role"
    
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)  # Role name (e.g., 'admin', 'user')
    description = db.Column(db.String(255))      # Role description

# Define User Model
class User(db.Model, UserMixin):
    __tablename__ = "user"
    
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)       # Required by Flask-Security
    confirmed_at = db.Column(db.DateTime())              # Confirmation timestamp
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))  # Many-to-many relationship with Role
    type = db.Column(db.String(20), default="general")
    full_name = db.Column(db.String(20), nullable=False)
    qualification = db.Column(db.String(20), nullable=False)
    DOB = db.Column(db.String(20), nullable=False)
    scores = db.Column(db.Integer(), db.ForeignKey("scores.id"))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)  # Required by Flask-Security

    def __repr__(self):
        return f"User('{self.id}','{self.email}','{self.type}','{self.full_name}')"

# Define the association table for the many-to-many relationship between User and Role
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)



# Define Subject Model
class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(80), unique=True)
    domain = db.Column(db.String(80), nullable=False)
    chapter = db.relationship("Chapter", backref="subject", lazy=True)
    quiz = db.relationship("Quiz", backref="subject", lazy=True)
    question = db.relationship("Questions", backref="subject", lazy=True)

    def __repr__(self):
        return f"Subject('{self.id}','{self.name}','{self.description}','{self.domain}')"

# Define Chapter Model
class Chapter(db.Model):
    __tablename__ = "chapter"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    subject_id = db.Column(db.Integer(), db.ForeignKey("subject.id"))
    description = db.Column(db.Text())
    quiz = db.relationship("Quiz", backref="chapter", lazy=True)
    question = db.relationship("Questions", backref="chapter", lazy=True)

    def __repr__(self):
        return f"Chapter('{self.id}','{self.name}','{self.subject_id}','{self.description}')"

# Define Quiz Model
class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    chapter_id = db.Column(db.Integer(), db.ForeignKey("chapter.id"))
    subject_id = db.Column(db.Integer(), db.ForeignKey("subject.id"))
    date_of_quiz = db.Column(db.String(20))
    time_duration = db.Column(db.String(20))
    remarks = db.Column(db.Text())
    question = db.relationship("Questions", backref="quiz", lazy=True)
    scores = db.relationship("Scores", backref="quiz", lazy=True)
    no_of_questions = db.Column(db.Integer())
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Quiz('{self.id}','{self.chapter_id}','{self.subject_id}','{self.date_of_quiz}','{self.time_duration}','{self.remarks}','{self.no_of_questions}','{self.name}')"

# Define Questions Model
class Questions(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer(), db.ForeignKey("quiz.id"))
    chapter_id = db.Column(db.Integer(), db.ForeignKey("chapter.id"))
    subject_id = db.Column(db.Integer(), db.ForeignKey("subject.id"))
    question_title = db.Column(db.Text(), nullable=False)
    question_statement = db.Column(db.Text(), nullable=False)
    option_1 = db.Column(db.String(50), nullable=False)
    option_2 = db.Column(db.String(50), nullable=False)
    option_3 = db.Column(db.String(50), nullable=False)
    option_4 = db.Column(db.String(50), nullable=False)
    correct_option = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Questions('{self.id}','{self.quiz_id}','{self.chapter_id}','{self.subject_id}','{self.question_title}','{self.question_statement}','{self.option_1}','{self.option_2}','{self.option_3}','{self.option_4}','{self.correct_option}')"

# Define Scores Model
class Scores(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer(), db.ForeignKey("quiz.id"))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    time_stamp_of_attempt = db.Column(db.DateTime(), default=datetime.utcnow)
    total_scored = db.Column(db.Integer())
    no_of_questions = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f"Scores('{self.id}','{self.quiz_id}','{self.user_id}','{self.time_stamp_of_attempt}','{self.total_scored}','{self.no_of_questions}')"