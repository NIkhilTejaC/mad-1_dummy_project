# from .database import db

# class User(db.Model):
#     id = db.Column(db.Integer() , primary_key = True)
#     email = db.Column(db.String(80) , nullable = False , unique = True)
#     password = db.Column(db.String(20) , nullable = False )
#     type = db.Column(db.String(20) , default ="general")
#     full_name = db.Column(db.String(20) , nullable = False )
#     qualification = db.Column(db.String(20) , nullable = False )
#     DOB = db.Column(db.String(20) , nullable = False )
    
# def __repr__(self): # This tells how our project is printed 
#     return f"User('{self.email}','{self.full_name}','{self.qualification}')"

from app import *    
    
    
class User(db.Model):
    
    __tablename__ = "user"
    
    id = db.Column(db.Integer() , primary_key = True , autoincrement = True)
    email = db.Column(db.String(80) , nullable = False , unique = True)
    password = db.Column(db.String(20) , nullable = False )
    type = db.Column(db.String(20) , default ="general")
    full_name = db.Column(db.String(20) , nullable = False )
    qualification = db.Column(db.String(20) , nullable = False )
    DOB = db.Column(db.String(20) , nullable = False )
    
def __repr__(self): # This tells how our project is printed 
    return f"User('{self.id}',{self.email}','{self.password}','{self.type}','{self.full_name}','{self.qualification}','{self.DOB}')"
    
with app.app_context():
    db.create_all()    