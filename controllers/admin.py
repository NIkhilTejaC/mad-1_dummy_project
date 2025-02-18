from flask import Blueprint, render_template, redirect, request, flash , url_for
from flask_login import login_required
from application.models1 import *
from flask_security.decorators import roles_required

# Create a Blueprint for admin routes
admin_bp = Blueprint('admin', __name__)



                                    ########### ADMIN ############


            ############ ADMIN DASHBOARD ##########
            
@admin_bp.route('/admin_dashboard')
# @roles_required('admin')  # Only users with the 'admin' role can access this route
def admin_dashboard():
    sub = Subject.query.all()
    chp = Chapter.query.all()
    return render_template('admin/admin_dashboard.html' , subject = sub , chapter = chp)


            ######### SUBJECT ############

@admin_bp.route('/admin_add_subject' , methods = ['GET' , 'POST'])
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
          
    return render_template('admin/admin_add_subject.html')


@admin_bp.route('/admin_delete_subject/<int:id>', methods=['GET' , 'POST'])
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
    
    return render_template('admin/admin_dashboard.html')

@admin_bp.route('/admin_edit_subject/<int:id>', methods=['GET' , 'POST'])
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
        
    return render_template('admin/admin_edit_subject.html' ,id = id )
           
  


                     ######### CHAPTER ############
            
@admin_bp.route('/admin_add_chapter/<int:subject_id>', methods=['GET' , 'POST'])
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
        
    return render_template('admin/admin_add_chapter.html', subject_id = subject_id)


@admin_bp.route('/admin_delete_chapter/<int:id>', methods=['GET' , 'POST'])
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
    
    return render_template('admin/admin_dashboard.html')

                ######## EDIT CHAPTER ########

@admin_bp.route('/admin_edit_chapter/<int:id>', methods=['GET' , 'POST'])
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
        
    return render_template('admin/admin_edit_chapter.html' ,id = id )
           


                                             ############################    
                                             ############ QUIZ ##########
                                             ############################   

            ######### ADD QUIZ ############
            
@admin_bp.route('/admin_add_quiz', methods=['GET' , 'POST'])
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
        
    return render_template('admin/admin_add_quiz.html')



@admin_bp.route('/admin_delete_quiz/<int:id>', methods=['GET' , 'POST'])
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

    return render_template('admin/admin_quiz.html')


@admin_bp.route('/admin_edit_quiz/<int:id>', methods=['GET' , 'POST'])
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
        
    return render_template('admin/admin_edit_quiz.html' ,id = id , qz = qz)



                                                 ###########################    
                                                 ###      QUESTION       ###
                                                 ###########################   
            
@admin_bp.route('/admin_add_question/<int:subject_id>/<int:chapter_id>/<int:quiz_id>', methods=['GET' , 'POST'])
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
        
    return render_template('admin/admin_add_question.html')


@admin_bp.route('/admin_delete_question/<int:id>', methods=['GET' , 'POST'])
def admin_delete_question(id):
    
    ques = Questions.query.get(id)
    
    db.session.delete(ques)
    db.session.commit()

    return render_template('admin_quiz.html')


@admin_bp.route('/admin_edit_question/<int:id>', methods=['GET' , 'POST'])
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
        
    return render_template('admin/admin_edit_question.html' ,id = id , ques = ques)



            ######### ADMIN QUIZ ############

@admin_bp.route('/admin_quiz')
def admin_quiz():
    quiz = Quiz.query.all()
    question = Questions.query.all()
    chapter = Chapter.query.all()
    subject = Subject.query.all()
    return render_template('admin/admin_quiz.html' , quiz = quiz , question = question , chapter = chapter , subject = subject) 


            ######### ADMIN SUMMARY ############

@admin_bp.route('/admin_summary')
def admin_summary():
    quiz = Quiz.query.all()
    question = Questions.query.all()
    chapter = Chapter.query.all()
    subject = Subject.query.all()
    user = User.query.all()
    scores = Scores.query.all()
    return render_template('admin/admin_summary.html',quiz = quiz , question = question , chapter = chapter , subject = subject , scores = scores,user=user)    

