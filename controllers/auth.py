from flask import Blueprint, render_template, redirect, request, url_for, session, flash
from flask_login import login_user, logout_user, login_required
from application.models1 import User, db

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/")
def login():
    return redirect('/home')

@auth_bp.route("/home")
def home():
    return render_template('auth/home.html')

@auth_bp.route('/user_login', methods=['GET', 'POST'])
def user_login():
    error_login = None
    error_password = None
    
    if request.method == 'POST':
        u_email = request.form.get("u_email")
        session['email'] = request.form.get("u_email")
        pwd = request.form.get("pwd")
        this_user = User.query.filter_by(email=u_email).first()
        if this_user:
            if this_user.password == pwd:
                if this_user.type == "admin":
                    login_user(this_user)
                    return redirect('/admin_dashboard')
                else:
                    login_user(this_user)
                    return redirect(f'/user_dashboard/{this_user.id}')
            else:
                error_password = "Incorrect Password !!!"
        else:
            error_login = "User Does not Exist !!!"
    
    return render_template('auth/login.html', error_login=error_login, error_password=error_password)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u_email = request.form.get("u_email")
        pwd = request.form.get("pwd")
        name = request.form.get("name")
        qual = request.form.get("qual")
        dob = request.form.get("dob")
        
        this_user = User.query.filter_by(email=u_email).first()
        if this_user:
            return "User already exists !!!"
        else:
            new_user = User(email=u_email, password=pwd, full_name=name, qualification=qual, DOB=dob)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/user_login')
    return render_template('auth/registration.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    logout_user()
    return render_template('auth/home.html')