from flask import Flask , request , flash
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager , UserMixin , login_user , logout_user , login_required
# from key import secret_key

from datetime import timedelta

app = Flask(__name__) 
app.secret_key = "secret_key"
app.permanent_session_lifetime = timedelta(minutes=10)
# print(secret_key)
# login_manager = LoginManager()
# login_manager.init_app(app)

app.debug = True     
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db" 
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


# # Create a timedelta object representing 10 minutes
# ten_minutes = timedelta(minutes=10)

# # Example usage (assuming you have a variable named `app`)
# app.permanent_session_lifetime = ten_minutes

                           ###### models.py #############

                        #  All the Tables are defined here 


class User(db.Model , UserMixin):
    
    __tablename__ = "user"
    
    id = db.Column(db.Integer() , primary_key = True , autoincrement = True)
    email = db.Column(db.String(80) , nullable = False , unique = True)
    password = db.Column(db.String(20) , nullable = False )
    type = db.Column(db.String(20) , default ="general")
    full_name = db.Column(db.String(20) , nullable = False )
    qualification = db.Column(db.String(20) , nullable = False )
    DOB = db.Column(db.String(20) , nullable = False )
    scores = db.Column(db.Integer() , db.ForeignKey("scores.id"))
    # is_active = db.Column(db.Boolean() , default = True )
    
def __repr__(self): # This tells how our project is printed 
    return f"User('{self.id}','{self.email}','{self.password}','{self.type}','{self.full_name}','{self.qualification}','{self.DOB}' , '{self.scores}')"

                               ##### SUBJECT #########

class Subject(db.Model):
    
    __tablename__ = "subject"
    
    id = db.Column(db.Integer() , primary_key = True , autoincrement = True)
    name = db.Column(db.String(80) , nullable = False , unique = True)
    # topic = db.Column(db.String(80) , nullable = False )
    description = db.Column(db.String(80) , unique = True)
    chapter = db.relationship("Chapter", backref="subject" , lazy=True)
    domain = db.Column(db.String(80) , nullable = False )
    quiz = db.relationship("Quiz", backref="subject" , lazy=True)
    question = db.relationship("Questions", backref="subject" , lazy=True)
    # level = db.Column(db.String(20) , nullable = False )
    # difficulty = db.Column(db.String(20) , nullable = False )
    # no_of_questions = db.Column(db.Integer())

def __repr__(self): # This tells how our project is printed 
    return f"Subject('{self.id}','{self.name}','{self.description}','{self.chapter}','{self.domain}','{self.quiz}','{self.question}')"

                            ########### CHAPTER #########

class Chapter(db.Model):
    
    __tablename__ = "chapter"
    
    id = db.Column(db.Integer() , primary_key = True , autoincrement = True)
    name = db.Column(db.String(80) , nullable = False , unique = True)
    # topic = db.Column(db.String(80) , nullable = False )
    subject_id = db.Column(db.Integer() , db.ForeignKey("subject.id"))
    description = db.Column(db.Text())
    quiz = db.relationship("Quiz", backref="chapter" , lazy=True)
    question = db.relationship("Questions", backref="chapter" , lazy=True)
    # branch = db.Column(db.String(80) , nullable = False )
    # level = db.Column(db.String(20) , nullable = False )
    # difficulty = db.Column(db.String(20) , nullable = False )
    # no_of_questions = db.Column(db.Integer())

def __repr__(self): # This tells how our project is printed 
    return f"Chapter('{self.id}','{self.name}','{self.subject_id}','{self.description}','{self.quiz}','{self.question}')"

                            ####### QUIZ #######
                            
class Quiz(db.Model):
    
    __tablename__ = "quiz"
    
    id = db.Column(db.Integer() , primary_key = True , autoincrement = True)
    chapter_id = db.Column(db.Integer() , db.ForeignKey("chapter.id"))
    subject_id = db.Column(db.Integer() , db.ForeignKey("subject.id"))
    date_of_quiz = db.Column(db.String(20))  # Represents dates (year, month, day).
    time_duration = db.Column(db.String(20)) #  Represents time (hours, minutes, seconds).
    remarks = db.Column(db.Text())
    question = db.relationship("Questions" , backref="quiz" , lazy = True)
    scores = db.relationship("Scores" , backref="quiz" , lazy = True)
    no_of_questions = db.Column(db.Integer())
    name = db.Column(db.String(20) , nullable = False)
    
    
    
def __repr__(self): # This tells how our project is printed 
    return f"Quiz('{self.id}','{self.chapter_id}','{self.subject_id}','{self.date_of_quiz}','{self.time_duration}','{self.remarks}','{self.question}','{self.scores}','{self.no_of_questions}','{self.name}')"

                    ############# QUESTIONS ###############
 
class Questions(db.Model):
    
    __tablename__ = "question"
    
    id = db.Column(db.Integer() , primary_key = True , autoincrement = True)
    quiz_id = db.Column(db.Integer() , db.ForeignKey("quiz.id"))
    chapter_id = db.Column(db.Integer() , db.ForeignKey("chapter.id"))
    subject_id = db.Column(db.Integer() , db.ForeignKey("subject.id"))
    question_title = db.Column(db.Text() , nullable = False)
    question_statement = db.Column(db.Text() , nullable = False) #db.Text(): Represents large text data without a size limit.
    option_1 = db.Column(db.String(50) , nullable = False)
    option_2 = db.Column(db.String(50) , nullable = False)
    option_3 = db.Column(db.String(50) , nullable = False)
    option_4 = db.Column(db.String(50) , nullable = False)
    correct_option = db.Column(db.String(50) , nullable = False)
    
def __repr__(self): # This tells how our project is printed 
    return f"Questions('{self.id}',{self.quiz_id}','{self.chapter_id}','{self.subject_id}','{self.question_title}','{self.question_statement}','{self.option_1}','{self.option_2}','{self.option_3}','{self.option_4}','{self.correct_option}')"
                   
                   
                   ############### SCORES ##################
from datetime import datetime
                   
class Scores(db.Model):
    
    __tablename__ = "scores"
    
    id = db.Column(db.Integer() , primary_key = True , autoincrement = True)
    quiz_id = db.Column(db.Integer() , db.ForeignKey("quiz.id"))
    user_id = db.Column(db.Integer() , db.ForeignKey("user.id"))
    time_stamp_of_attempt = db.Column(db.DateTime() , default = datetime.utcnow)#'YYYY-MM-DD HH:MM:SS'
    total_scored = db.Column(db.Integer())
    no_of_questions = db.Column(db.Integer(),nullable = False)
    
def __repr__(self): # This tells how our project is printed 
    return f"Scores('{self.id}','{self.quiz_id}','{self.user_id}','{self.time_stamp_of_attempt}','{self.total_scored}','{self.no_of_questions}')"
                                   



                   ############# models.py ends here ###############


with app.app_context():
    db.create_all()    
       
# from application.models import *       
       
app.app_context().push() 




from application.controllers1 import * 

if __name__ == "__main__":
    app.run()