from flask import Flask , request
#from application.database import db
from flask_sqlalchemy import SQLAlchemy

#from application.resources import api 



app = Flask(__name__) # app is an object and is linked to app.py through this statement
app.debug = True      # '__name__' refers to current module(retrieves name of fie ) and is a constructor in python and defined name 
    
    # URI for the database id the place where it is located
    # "///" means a relative path from the current file 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///quiz.db" 
db = SQLAlchemy(app)
#db.init_app(app) # The application should be configured with the db object
    
#api.init_app(app) # Initializing the api object

class User(db.Model):
    id = db.Column(db.Integer() , primary_key = True)
    email = db.Column(db.String(80) , nullable = False , unique = True)
    password = db.Column(db.String(20) , nullable = False )
    type = db.Column(db.String(20) , default ="general")
    full_name = db.Column(db.String(20) , nullable = False )
    qualification = db.Column(db.String(20) , nullable = False )
    DOB = db.Column(db.String(20) , nullable = False )
    
def __repr__(self): # This tells how our project is printed 
    return f"User('{self.email}','{self.full_name}','{self.qualification}')"
    
    
    
app.app_context().push() # This makes sure that the server code is taken from app.py file 
    

with app.app_context():
    db.create_all()


from application.controllers import * 

if __name__ == "__main__":
    app.run()