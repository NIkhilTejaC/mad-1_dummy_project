# We will have all the routes here 

from flask import Flask , render_template , redirect , request , url_for , session
from flask import current_app as app 

from app import *

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)

# base URL - 127.0.0.1:5000

@app.route("/")
def login():

    return redirect('/home')

@app.route("/home")
def home():

    return render_template('home.html')



@app.route('/login' , methods = ['GET' , 'POST'])
def user_login():
    error_login = None
    error_password = None
    
    if request.method == 'POST':
        u_email = request.form.get("u_email")
        session['email'] = request.form.get("u_email")
        pwd = request.form.get("pwd")
        print(u_email , pwd)
        this_user = User.query.filter_by(email = u_email).first() # .first() gives only the first matching row rather than all unlike ".all()"
        if this_user: # if this_user exists
            # this_user is a fetch object
            if this_user.password == pwd:##   if this_user.password == hash(pwd):
                if this_user.type == "admin":## Verifying with the hash
                    login_user(this_user) 
                    return redirect('/admin_dashboard') 
                else:
                    print(this_user.id)
                    login_user(this_user)
                    return redirect(f'/user_dashboard/{this_user.id}')
                    #return redirect(f'/user/{this_user.id}')
            else:
                error_password = "Incorrect Password !!!"
                # return "Incorrect password" #flash('Incorrect Password !', 'error')
        else: # if this_user has value "None"
            error_login = "User Does not Exist !!!"
            # return "user does not exist"  
      
    return render_template('login.html' , error_login = error_login , error_password = error_password ) # No need to add '/templates/' because Flask by default will look for folder named 'templates'
# We need to specifically mention if the method is 'POST'




@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    ### First thing to check !!!
    ### To check whether the user already exists or not 
    if request.method == 'POST':
        u_email = request.form.get("u_email")
        pwd = request.form.get("pwd")
        name = request.form.get("name")
        qual = request.form.get("qual")
        dob = request.form.get("dob")
        
        this_user = User.query.filter_by(email = u_email).first()
        if this_user:
            return "User already exists !!!"
        else:
            new_user = User(email = u_email , password = pwd , full_name = name , qualification = qual , DOB = dob) ## add the hash 'hash(pwd)'
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
    return render_template('registration.html')

                                    ########### ADMIN ############


            ############ ADMIN DASHBOARD ##########
            
@app.route('/admin_dashboard')
def admin_dashboard():
    sub = Subject.query.all()
    chp = Chapter.query.all()
    return render_template('admin_dashboard.html' , subject = sub , chapter = chp)


            ######### SUBJECT ############

@app.route('/admin_add_subject' , methods = ['GET' , 'POST'])
def admin_add_subject():
    if request.method == 'POST':
        name = request.form.get("name")
        description = request.form.get("description")
        domain = request.form.get("domain")
        
        this_subject = Subject.query.filter_by(name = name).first()
        if this_subject:
            return "Subject already exists !!!"
        else:
            sub = Subject(name = name , description = description , domain = domain)
            db.session.add(sub)
            db.session.commit()
            return redirect('/admin_dashboard')
          
    return render_template('admin_add_subject.html')


@app.route('/admin_delete_subject/<int:id>', methods=['GET' , 'POST'])
def admin_delete_subject(id):
    
    sub = Subject.query.get(id)
    
    db.session.delete(sub)
    db.session.commit()
    
    chapter = Chapter.query.all()
    quiz = Quiz.query.all()
    question = Questions.query.all()
    
    for chp in chapter:
        if chp.subject_id == id:
            db.session.delete(chp)
            db.session.commit()
    
    for q in quiz:
        if q.chapter_id == id:
            db.session.delete(q)
            db.session.commit()
    
    for ques in question:
        if ques.chapter_id == id:
            db.session.delete(ques)
            db.session.commit()
    
    return render_template('admin_dashboard.html')

@app.route('/admin_edit_subject/<int:id>', methods=['GET' , 'POST'])
def admin_edit_subject(id):
    if request.method == 'POST':
        name = request.form.get("name")
        description = request.form.get("description")
        domain = request.form.get("domain")
        
        s = Subject.query.filter_by(id = id).first()
        s.name = name 
        s.description = description 
        s.domain = domain
        db.session.commit()
        
        return redirect('/admin_dashboard')
        
    return render_template('admin_edit_subject.html' ,id = id )
           
  


                     ######### CHAPTER ############
            
@app.route('/admin_add_chapter/<int:subject_id>', methods=['GET' , 'POST'])
def admin_add_chapter(subject_id):
    
    if request.method == 'POST':
        name = request.form.get("name")
        subject_id = subject_id
        description = request.form.get("description")
        
        this_chapter = Subject.query.filter_by(id = subject_id).first()
        if not this_chapter:
            return "Subject does not exist !!!"
        else:
            subject = Subject.query.get_or_404(subject_id)
            chp = Chapter(name = name ,subject_id = subject_id,  description = description , subject = subject)
            db.session.add(chp)
            db.session.commit()
            return redirect('/admin_dashboard')
        
    return render_template('admin_add_chapter.html', subject_id = subject_id)


@app.route('/admin_delete_chapter/<int:id>', methods=['GET' , 'POST'])
def admin_delete_chapter(id):
    
    chp = Chapter.query.get(id)
    
    db.session.delete(chp)
    db.session.commit()
    
    quiz = Quiz.query.all()
    question = Questions.query.all()
    
    for q in quiz:
        if q.chapter_id == id:
            db.session.delete(q)
            db.session.commit()
    
    for ques in question:
        if ques.chapter_id == id:
            db.session.delete(ques)
            db.session.commit()
    
    return render_template('admin_dashboard.html')

                ######## EDIT CHAPTER ########

@app.route('/admin_edit_chapter/<int:id>', methods=['GET' , 'POST'])
def admin_edit_chapter(id):
    if request.method == 'POST':
        name = request.form.get("name")
        subject_id =  request.form.get("sid")
        chapter_id = id
        description = request.form.get("description")
        
        c = Chapter.query.filter_by(id = id).first()
        c.name = name 
        c.subject_id = subject_id 
        c.description = description 
        db.session.commit()
        
        return redirect('/admin_dashboard')
        
    return render_template('admin_edit_chapter.html' ,id = id )
           


                                             ############################    
                                             ############ QUIZ ##########
                                             ############################   

            ######### ADD QUIZ ############
            
@app.route('/admin_add_quiz', methods=['GET' , 'POST'])
def admin_add_quiz():
    
    if request.method == 'POST':
        subject_id = request.form.get("subject_id")
        chapter_id = request.form.get("chapter_id")
        date_of_quiz = request.form.get("doq")
        time_duration = request.form.get("toq")
        remarks = request.form.get("remark")
        no_of_questions = request.form.get("noq")
        name = request.form.get("name")
        
        ### Time Duration
        
        
            
        
        this_quiz = Chapter.query.filter_by(id = chapter_id).first()
        if not this_quiz:
            return "Chapter does not exist !!!"
        else:
            subject = Subject.query.get_or_404(subject_id)
            chapter = Chapter.query.get_or_404(chapter_id)
            quiz = Quiz(chapter_id = chapter_id , subject_id = subject_id  , date_of_quiz = date_of_quiz ,  time_duration = time_duration , remarks = remarks , no_of_questions = no_of_questions ,name = name , subject = subject , chapter = chapter)
            db.session.add(quiz)
            db.session.commit()
            return redirect('/admin_quiz')
        
    return render_template('admin_add_quiz.html')



@app.route('/admin_delete_quiz/<int:id>', methods=['GET' , 'POST'])
def admin_delete_quiz(id):
    
    q = Quiz.query.get(id)
    
    db.session.delete(q)
    db.session.commit()
    
    # return redirect(url_for('/admin_delete_quiz' , id = id))
    
    question = Questions.query.all()
    
    for ques in question:
        if ques.quiz_id == id:
            db.session.delete(ques)
            db.session.commit()

    return render_template('admin_quiz.html')


@app.route('/admin_edit_quiz/<int:id>', methods=['GET' , 'POST'])
def admin_edit_quiz(id):
    qz = Quiz.query.get(id)
    if request.method == 'POST':
        subject_id = request.form.get("subject_id")
        chapter_id = request.form.get("chapter_id")
        date_of_quiz = request.form.get("doq")
        time_duration = request.form.get("toq")
        remarks = request.form.get("remark")
        no_of_questions = request.form.get("noq")
        name = request.form.get("name")
        
        q = Quiz.query.filter_by(id = id).first()
        q.subject_id = subject_id 
        q.chapter_id = chapter_id 
        q.date_of_quiz = date_of_quiz 
        q.time_duration = time_duration
        q.remarks = remarks 
        q.no_of_questions = no_of_questions 
        q.name = name 
        db.session.commit()
        
        return redirect('/admin_quiz')
        
    return render_template('admin_edit_quiz.html' ,id = id , qz = qz)



                                                 ###########################    
                                                 ###      QUESTION       ###
                                                 ###########################   
            
@app.route('/admin_add_question/<int:subject_id>/<int:chapter_id>/<int:quiz_id>', methods=['GET' , 'POST'])
def admin_add_question(subject_id , chapter_id , quiz_id):
    
    if request.method == 'POST':
        subject_id = subject_id
        chapter_id = chapter_id
        quiz_id = quiz_id
        question_title = request.form.get("qt")
        question = request.form.get("qs")
        o1 = request.form.get("option_1")
        o2 = request.form.get("option_2")
        o3 = request.form.get("option_3")
        o4 = request.form.get("option_4")
        correct_option = request.form.get("correct_option")
        
        list = [o1,o2,o3,o4]
        n = 0
        c = 0
        if correct_option == o1:
            correct_option = "option_1"
            
        if correct_option == o2:
            correct_option = "option_2"
            
        if correct_option == o3:
            correct_option = "option_3"
            
        if correct_option == o4:
            correct_option = "option_4"        
        
        this_quiz = Quiz.query.filter_by(id = quiz_id).first()
        this_chapter = Chapter.query.filter_by(id = chapter_id).first()
        if not ( this_quiz and this_chapter ):
            return "Either Subject or Chapter does not exist !!!"
        else:
            subject = Subject.query.get_or_404(subject_id)
            chapter = Chapter.query.get_or_404(chapter_id)
            quiz = Quiz( id = quiz_id )
            ques = Questions(quiz_id = quiz_id , chapter_id = chapter_id,subject_id = subject_id ,question_title = question_title,  question_statement = question , option_1 = o1 , option_2 = o2 , option_3 = o3 , option_4 = o4 , correct_option = correct_option)
            db.session.add(ques)
            db.session.commit()
            return redirect('/admin_quiz')
        
    return render_template('admin_add_question.html')


@app.route('/admin_delete_question/<int:id>', methods=['GET' , 'POST'])
def admin_delete_question(id):
    
    ques = Questions.query.get(id)
    
    db.session.delete(ques)
    db.session.commit()

    return render_template('admin_quiz.html')


@app.route('/admin_edit_question/<int:id>', methods=['GET' , 'POST'])
def admin_edit_question(id):
    ques = Questions.query.get(id)
    if request.method == 'POST':
        subject_id = request.form.get("subject_id")
        chapter_id = request.form.get("chapter_id")
        quiz_id = request.form.get("quiz_id")
        question_title = request.form.get("qt")
        question = request.form.get("qs")
        o1 = request.form.get("option_1")
        o2 = request.form.get("option_2")
        o3 = request.form.get("option_3")
        o4 = request.form.get("option_4")
        correct_option = request.form.get("correct_option")
        
        q = Questions.query.filter_by(id = id).first()
        q.subject_id = subject_id 
        q.chapter_id = chapter_id 
        q.quiz_id = quiz_id 
        q.question_title = question_title 
        q.question_statement = question
        q.option_1 = o1
        q.option_2 = o2
        q.option_3 = o3 
        q.option_4 = o4 
        q.correct_option = correct_option
        db.session.commit()
        
        return redirect('/admin_quiz')
        
    return render_template('admin_edit_question.html' ,id = id , ques = ques)



            ######### ADMIN QUIZ ############

@app.route('/admin_quiz')
def admin_quiz():
    quiz = Quiz.query.all()
    question = Questions.query.all()
    chapter = Chapter.query.all()
    subject = Subject.query.all()
    return render_template('admin_quiz.html' , quiz = quiz , question = question , chapter = chapter , subject = subject) 


            ######### ADMIN SUMMARY ############

@app.route('/admin_summary')
def admin_summary():
    quiz = Quiz.query.all()
    question = Questions.query.all()
    chapter = Chapter.query.all()
    subject = Subject.query.all()
    user = User.query.all()
    scores = Scores.query.all()
    return render_template('admin_summary.html',quiz = quiz , question = question , chapter = chapter , subject = subject , scores = scores,user=user)    


                                                ################
                                        ########## USER DASHBOARD #############    
                                                ################

from datetime import datetime
import pytz

@app.route('/user_dashboard/<int:user_id>', methods=['GET' , 'POST']) 
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
        
    
    return render_template('user_dashboard.html', user = user ,quiz = quiz , question = question , chapter = chapter , subject = subject , scores = scores, c = c)   

                                     ######### USER QUIZ - VIEW ############

@app.route('/user_quiz_view/<int:user_id>/<int:quiz_id>', methods=['GET' , 'POST']) 
def user_quiz_view(user_id,quiz_id):
    quiz = Quiz.query.get(quiz_id)
    question = Questions.query.all()
    chapter = Chapter.query.all()
    subject = Subject.query.all()
    scores = Scores.query.all()
    user = User.query.get(user_id)
    
    return render_template('user_quiz_view.html' ,quiz = quiz , question = question , chapter = chapter , subject = subject , scores = scores)   



                                    ######### USER QUIZ - START ############

from datetime import timedelta , datetime

@app.route('/user_quiz_start/<int:user_id>/<int:quiz_id>', methods=['GET' , 'POST']) 
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
        
    
    return render_template('user_quiz_start.html', user = user ,quiz = quiz , question = qs , chapter = chapter , subject = subject , scores = scores , score = 0 ,count = 1 , timer_duration=session['timer_duration'] )   

                                 ######### USER QUIZ - START - CHECK ############

@app.route('/user_quiz_start_check/<int:user_id>/<int:question_id>/<int:score>/<int:count>', methods=['GET' , 'POST']) 
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
            return redirect(url_for('user_quiz_end_submit', user_id=user_id, quiz_id = quiz_id, score=score))    
        
    qs = Questions.query.filter_by(id=question_id).first()
    
    return render_template('user_quiz_start.html', user = user ,quiz = q , question = qs , chapter = chapter , subject = subject , scores = scores , score = score , count = count ,timer_duration=session['timer_duration'] )   



                            ######### USER QUIZ - END - SUBMIT ############
                            
@app.route('/user_quiz_end_submit/<int:user_id>/<int:quiz_id>/<int:score>', methods=['GET','POST'])
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

    return render_template('user_summary.html',user = user  , chapter = chapter , subject = subject , scores = scores)






                                     ######### USER SCORES ############

@app.route('/user_scores/<int:user_id>') 
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
        
    
    return render_template('user_scores.html' ,user = user,quiz = quiz , question = question , chapter = chapter , subject = subject , scores = scores )   

                                    ######### USER SUMMARY ############
    
@app.route('/user_summary/<int:user_id>') 
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
        
        
        
    
    
    return render_template('user_summary.html', user = user , scores = scores , quiz = quiz , question = question , chapter = chapter , subject = subject) 

                                    ######### USER PROFILE ############

@app.route('/user_profile/<int:user_id>') 
def user_profile(user_id):
    user = User.query.get(user_id)
    return render_template('user_profile.html' , user = user)    


@app.route('/user_profile_edit/<int:user_id>' , methods=['POST','GET']) 
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
        user.qualification = qualification
        user.DOB = dob
        
        db.session.commit()
        
        return render_template('user_profile.html' , user = user)
    
    return render_template('user_profile_edit.html' , user = user)    


   
    
                                                 ################
                                        ########## LOGOUT #############    
                                                ################

    
@app.route('/logout')
def logout():
    session.pop('username', None)
    logout_user()
    return render_template('home.html')