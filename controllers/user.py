from flask import Blueprint, render_template, redirect, request, session , url_for
from flask_login import login_required, current_user
from application.models1 import *
from datetime import datetime
import pytz

# Create a Blueprint for user routes
user_bp = Blueprint('user', __name__)




                                                ################
                                        ########## USER DASHBOARD #############    
                                                ################

from datetime import datetime
import pytz

@user_bp.route('/user_dashboard/<int:user_id>', methods=['GET' , 'POST']) 
@login_required
def user_dashboard(user_id):
    quiz = Quiz.query.all()
    question = Questions.query.all()
    chapter = Chapter.query.all()
    subject = Subject.query.all()
    scores = Scores.query.all()
    user = User.query.get(user_id)
    
    dt = []
    for q in quiz: 
        date_format = "%Y-%m-%d"
        date1 = datetime.strptime(q.date_of_quiz, date_format).date()
        dt.append(date1)
    
        # Get the current time in IST
    ist_timezone = pytz.timezone('Asia/Kolkata')
    current_time_ist = datetime.now(ist_timezone).date()
    
    
    c = []
    for d in dt:
        if d > current_time_ist:
            c.append(0)
        else:
            c.append(1)
        
    
    return render_template('user/user_dashboard.html', user = user ,quiz = quiz , question = question , chapter = chapter , subject = subject , scores = scores, c = c)   

                                     ######### USER QUIZ - VIEW ############

@user_bp.route('/user_quiz_view/<int:user_id>/<int:quiz_id>', methods=['GET' , 'POST']) 
def user_quiz_view(user_id,quiz_id):
    quiz = Quiz.query.get(quiz_id)
    question = Questions.query.all()
    chapter = Chapter.query.all()
    subject = Subject.query.all()
    scores = Scores.query.all()
    user = User.query.get(user_id)
    
    return render_template('user/user_quiz_view.html' ,quiz = quiz , question = question , chapter = chapter , subject = subject , scores = scores)   



                                    ######### USER QUIZ - START ############

from datetime import timedelta , datetime

@user_bp.route('/user_quiz_start/<int:user_id>/<int:quiz_id>', methods=['GET' , 'POST']) 
def user_quiz_start(user_id,quiz_id):
    
    q = Quiz.query.filter_by(id = quiz_id).first()
    # Pass the timer duration only on the first load
    t = q.time_duration
    
    def time_to_minutes(time_str):
            # Split the time string into hours, minutes, and seconds
            hours, minutes, seconds = map(int, time_str.split(':'))
            
            # Convert the total time to minutes
            total_minutes = hours * 60 + minutes + seconds / 60
    
            return total_minutes
        
    t = time_to_minutes(t)
    
    
    if 'timer_duration' not in session:
        td = int(t) * 60
        session['timer_duration'] = td # 5 minutes in seconds
    
    score = 0
    count = 1
  
    quiz = Quiz.query.get(quiz_id)
    chapter = Chapter.query.all()
    subject = Subject.query.all()
    scores = Scores.query.all()
    user = User.query.get(user_id)

    qs = Questions.query.filter_by(quiz_id=quiz_id).first()
        
    
    return render_template('user/user_quiz_start.html', user = user ,quiz = quiz , question = qs , chapter = chapter , subject = subject , scores = scores , score = 0 ,count = 1 , timer_duration=session['timer_duration'] )   

                                 ######### USER QUIZ - START - CHECK ############

@user_bp.route('/user_quiz_start_check/<int:user_id>/<int:question_id>/<int:score>/<int:count>', methods=['GET' , 'POST']) 
def user_quiz_start_check(user_id,question_id,score,count):
    
    # Decrease the timer based on elapsed time (passed from the frontend)
    elapsed_time = int(request.form.get('elapsed_time', 0))
    session['timer_duration'] -= elapsed_time
    # count = count+1
    # selected_option = "None"
    
    # quiz = Quiz.query.all()
    questions = Questions.query.all()
    chapter = Chapter.query.all()
    subject = Subject.query.all()
    scores = Scores.query.all()
    user = User.query.get(user_id)
    
    qs = Questions.query.filter_by(id=question_id).first()
    
    quiz_id = qs.quiz_id 
    q = Quiz.query.filter_by(id = quiz_id).first()
    
    if request.method == "POST":
        selected_option = request.form.get('answer')
    
        if qs.correct_option == selected_option:
            score = score + 1
            
        if q.no_of_questions >= count:
            question_id = question_id + 1
        else:
            return redirect(url_for('user.user_quiz_end_submit', user_id=user_id, quiz_id = quiz_id, score=score))    
        
    qs = Questions.query.filter_by(id=question_id).first()
    
    return render_template('user/user_quiz_start.html', user = user ,quiz = q , question = qs , chapter = chapter , subject = subject , scores = scores , score = score , count = count ,timer_duration=session['timer_duration'] )   



                            ######### USER QUIZ - END - SUBMIT ############
                            
@user_bp.route('/user_quiz_end_submit/<int:user_id>/<int:quiz_id>/<int:score>', methods=['GET','POST'])
def user_quiz_end_submit(user_id,quiz_id,score):
    
    # selected_option = "None"
    
    # q = Quiz.query.filter_by(id = quiz_id).first()
    # question = Questions.query.all()
    chapter = Chapter.query.all()
    subject = Subject.query.all()
    scores = Scores.query.all()
    user = User.query.get(user_id)
    
    # qs = Questions.query.filter_by(id=question_id).first()
    
    # quiz_id = qs.quiz_id 
    # q = Quiz.query.filter_by(id = quiz_id).first()
    
    quiz = Quiz.query.get_or_404(quiz_id)
    user = User.query.get_or_404(user_id)
    
    
    quiz_score = Scores(quiz_id = quiz_id , user_id = user.id  , total_scored = score , no_of_questions = quiz.no_of_questions , quiz = quiz )
    db.session.add(quiz_score)
    db.session.commit()

    return render_template('user/user_summary.html',user = user  , chapter = chapter , subject = subject , scores = scores)






                                     ######### USER SCORES ############

@user_bp.route('/user_scores/<int:user_id>') 
def user_scores(user_id):
    quiz = Quiz.query.all()
    question = Questions.query.all()
    chapter = Chapter.query.all()
    subject = Subject.query.all()
    scores = Scores.query.filter_by(user_id = user_id).all()
    user = User.query.get(user_id)
    
    for s in scores:   
        idi = s.id
        user = User.query.get(user_id)
        user.scores = idi
        db.session.commit()
        
    
    return render_template('user/user_scores.html' ,user = user,quiz = quiz , question = question , chapter = chapter , subject = subject , scores = scores )   

                                    ######### USER SUMMARY ############
    
@user_bp.route('/user_summary/<int:user_id>') 
def user_summary(user_id):
    user = User.query.get(user_id)
    scores = Scores.query.filter_by(user_id = user_id).all()
    quiz = Quiz.query.all()
    question = Questions.query.all()
    chapter = Chapter.query.all()
    subject = Subject.query.all()
    
    
    # sc = []
    # qu = []
    # chp = []
    # sub = []
    
    # for s in scores:
    #     sc.append(s.id)
    #     q = Quiz.query.filter_by(id=s.quiz_id).all()
    #     for qz in q:
    #         qu.append(qz.id)
    #         c = Chapter.query.filter_by(id=qz.chapter_id).all()
    #         for ch in c:
    #             chp.append(ch.id)
    #         s = Subject.query.filter_by(id=qz.subject_id).all()
    #         for cu in s:
    #             sub.append(cu.id)
    
    # scores_s = []
    # for a in sc:
    #     a_s = Scores.query.filter_by(user_id = user_id).all()
        
        
        
    
    
    return render_template('user/user_summary.html', user = user , scores = scores , quiz = quiz , question = question , chapter = chapter , subject = subject) 

                                    ######### USER PROFILE ############

@user_bp.route('/user_profile/<int:user_id>') 
def user_profile(user_id):
    user = User.query.get(user_id)
    return render_template('user/user_profile.html' , user = user)    


@user_bp.route('/user_profile_edit/<int:user_id>' , methods=['POST','GET']) 
def user_profile_edit(user_id):
    user = User.query.get(user_id)
    
    if request.method == 'POST':
        u_email = request.form.get("u_email")
        pwd = request.form.get("pwd")
        name = request.form.get("name")
        qual = request.form.get("qual")
        dob = request.form.get("dob")
        
        user.email = u_email 
        user.password = pwd
        user.full_name = name 
        user.qualification = qual
        user.DOB = dob
        
        db.session.commit()
        
        return render_template('user/user_profile.html' , user = user)
    
    return render_template('user/user_profile_edit.html' , user = user)    


   