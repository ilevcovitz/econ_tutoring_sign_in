import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, RadioField, HiddenField, DateField, DateTimeField, PasswordField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

#this secret key is only used internally by the app
app.config['SECRET_KEY'] = 'Secret Key Here' 

#this password is used to login to the sign in page and to create a master list of sign ins
login_password = "Login Password Here"

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hunterecon:tVUxNJ2M@hunterecon.mysql.pythonanywhere-services.com/hunterecon$econtutoring'
#below is connection to python anywhere db. Econtutoring is the name of database, hunterecon is the username/name of site. 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hunterecon:MySQL_PASSWORD@hunterecon.mysql.pythonanywhere-services.com/hunterecon$econtutoring'

#uncomment the next line to work from a localhost, econtutoring is the name of the database on the localhost
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/econtutoring'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

#parameters to prevent pythonanywhere timeouts. 
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

#the following classes are abstract database models using SQLAlchemy

#many to many table in db for courses/students relationships
enrollment_mapping = db.Table('enrollment_mapping',
db.Column('students_id', db.Integer, db.ForeignKey('students.id')),
db.Column('courses_id', db.Integer, db.ForeignKey('courses.id'))
)

class courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    catalog_num = db.Column(db.Integer)
    section = db.Column(db.Text)
    instructor = db.Column(db.Text)
    subject = db.Column(db.Text)
    code = db.Column(db.Integer)
    term = db.Column(db.Integer)

    #sign_ins relationship
    sign_ins = db.relationship('sign_ins', backref='courses')


class students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    empl_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    first = db.Column(db.Text)
    last = db.Column(db.Text)
    email = db.Column(db.Text)

    #creates a many to many mapping from students to courses based on entries of enrollment_mapping
    courses = db.relationship('courses', secondary=enrollment_mapping, backref=db.backref('students', lazy='dynamic'), lazy='dynamic')
    #sign in relationship
    sign_ins = db.relationship('sign_ins', backref='students')

class purposes(db.Model):
    __tablename__ = 'purposes'
    id = db.Column(db.Integer, primary_key=True)
    purpose = db.Column(db.Text)
    sign_ins = db.relationship('sign_ins', backref='purposes')

class sign_ins(db.Model):
    __tablename__ = 'sign_ins'
    id = db.Column(db.Integer, primary_key=True)
    students_id = db.Column(db.Integer, db.ForeignKey(students.id))
    courses_id = db.Column(db.Integer, db.ForeignKey(courses.id))
    empl_id = db.Column(db.Integer)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    purpose_id = db.Column(db.Integer, db.ForeignKey(purposes.id))

class pins(db.Model):
    __tablename__ = 'pins'
    id = db.Column(db.Integer, primary_key=True)
    courses_id = db.Column(db.Integer, db.ForeignKey(courses.id))
    pin = db.Column(db.Integer)

    course = db.relationship('courses', backref='pins')


#The following classes are models for online forms using WTF extension to Flask

class LoginForm(Form):
    password = PasswordField('Password')
    login_form_submitted = HiddenField(default = 1)
    submit = SubmitField('Log In')

class StudentSearch(Form):

    empl_id = StringField('Employee ID', validators=[])
    student_search_submitted = HiddenField(default = 1)
    submit = SubmitField('Search')

class SignIn(Form):
    purpose_choice = RadioField(label='Purpose', choices= [(1, "Drop-in"), (2, "Special Review Session: Quiz"), (3, "Special Review Session: Midterm 1"), (4, "Special Review Session: Midterm 2") ], default = 1, validators=[])
    student_courses = SelectField(label='Class', choices = [(0,"Not Available")], validators = [], coerce=int)
    sign_in_submitted = HiddenField(default = 1)
    submit = SubmitField('Sign In')

class AttendanceForm(Form):
    pin = StringField('Pin')
    attendance_form_submitted = HiddenField(default = 1)
    submit = SubmitField('Log In')

#register student class, same as SignIn, but accepts date and time. Inherits from SignIn class
class Register(SignIn):
    date = DateTimeField(label='Date/Time (Year-Month-Day Hour-Minute-Second)', default= datetime.today().date())
    submit = SubmitField('Register')

#page not found handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#server error handler
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



#index page handler. This is the page where students sign in. 
@app.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()


    if 'login_form_submitted' in request.form:
        entered_password = login_form.password.data

        if str(entered_password) == str(login_password):
            session['authenticated'] = True
            flash("Login Successful")
        else:
            session['authenticated'] = False
            flash("Incorrect Password")



    if session.get('authenticated') == True:

        #create new StudentSearch form
        search_form = StudentSearch(csrf_enabled=False)
        #create new SignIn form
        sign_in_form = SignIn()

        #list containing a student's classes
        if(session.get('student_courses')):
            student_courses = session.get('student_courses')
            #updates form to have student classes as well
            sign_in_form.student_courses.choices = student_courses

        #student search form was submitted
        if 'student_search_submitted' in request.form:
            print("SEARCH FORM VALIDATED")
            #Empl ID was correctly entered in form
            if search_form.empl_id.data:
                #creates a session and local variable with empl id
                session['empl_id'] = search_form.empl_id.data
                empl_id = search_form.empl_id.data

                #search students table for this student

                student = students.query.filter_by(empl_id = empl_id).first()

                #if a match is found
                if(student):
                    #create a new session list with student information
                    session['student_info'] = {'empl_id': empl_id,'students_id': student.id, 'first': student.first, 'last': student.last}

                    if(student.courses):
                        #student courses in a list of objects format
                        student_courses_objects = student.courses
                        print(student_courses_objects)
                        #loop through student courses creating a list with entries: courses_id, print string
                        #print string is text displayed in form
                        student_courses = []

                        for this_course in student_courses_objects:

                            #if an instructor is listed
                            if this_course.instructor:
                                instructor = this_course.instructor
                            else:
                                instructor = "NA"

                            print_string = this_course.subject + " " + str(this_course.catalog_num) + " Section: " + this_course.section + " Instructor: " + instructor
                            class_id = this_course.id

                            #add this course to courses list
                            student_courses.append([ class_id, print_string])

                        #add an option for not selecting a course
                        student_courses.append([0,"Not Available"])
                        session['student_courses'] = student_courses

                        flash("Student record located. Please fill in your information below and click \"Sign in\" to complete registration.")





                #No match for this empl id found
                else:
                    flash("No student with ID: " + session['empl_id'] + " found."  )
                    #clear session ID
                    session['empl_id'] = None

            #No Empl ID was entered
            else:
                flash("No Employee ID entered")

            #refresh page
            return redirect(url_for('index'))



        #signing a student in
        if 'sign_in_submitted' in request.form:
            print("SIGN IN FORM VALIDATED")
            #get student info from session variable
            student_info = session.get('student_info')

            if student_info != None:
                #create a sign in object with form data
                this_sign_in = sign_ins(students_id= student_info['students_id'], empl_id = student_info['empl_id'], purpose_id = sign_in_form.purpose_choice.data, courses_id = sign_in_form.student_courses.data , date = datetime.now().date(), time = datetime.now().time() )

                #add sign in to database
                db.session.add(this_sign_in)
                db.session.commit()

                #clear student data
                session['empl_id'] = None
                session['student_info'] = None
                session['student_courses'] = None

                flash("Sign In Successful")
            else:
                flash("No student found to sign in")

            return redirect(url_for('index'))


        #get today's sign ins
        todays_sign_ins_objects = sign_ins.query.filter_by(date = datetime.today().date()).all()
        todays_sign_ins = []
        count = 0
        if todays_sign_ins_objects:
            for this_sign_in in todays_sign_ins_objects:
                count = count + 1
                if this_sign_in.courses:
                    this_catalog_num = this_sign_in.courses.catalog_num
                    this_section = this_sign_in.courses.section
                    this_subject = this_sign_in.courses.subject
                else:
                    this_catalog_num = "NA"
                    this_section = "NA"
                    this_subject = ""

                todays_sign_ins.append(str(this_sign_in.time) + ", " + this_sign_in.students.first + " " + this_sign_in.students.last + ", " + this_subject + " " + str(this_catalog_num) + " Section: " + str(this_section))
        else:
            todays_sign_ins.append("No sign ins today.")
        #render HTML template
        return render_template('index.html', search_form=search_form, sign_in_form = sign_in_form, student_info = session.get('student_info'), todays_sign_ins = todays_sign_ins)

    else:
        return render_template('login.html', login_form = login_form)









#register old sign ins page
@app.route('/register', methods=['GET', 'POST'])
def register():

    login_form = LoginForm()


    if 'login_form_submitted' in request.form:
        entered_password = login_form.password.data

        if str(entered_password) == str(login_password):
            session['authenticated'] = True
            flash("Login Successful")
        else:
            session['authenticated'] = False
            flash("Incorrect Password")



    if session.get('authenticated') == True:
        #create new StudentSearch form
        search_form = StudentSearch(csrf_enabled=False)
        #create new Register form
        sign_in_form = Register()

        #list containing a student's classes
        if(session.get('student_courses')):
            student_courses = session.get('student_courses')
            #updates form to have student classes as well
            sign_in_form.student_courses.choices = student_courses


        #student search form was submitted
        if 'student_search_submitted' in request.form:
            print("SEARCH FORM VALIDATED")
            #Empl ID was correctly entered in form
            if search_form.empl_id.data:
                #creates a session and local variable with empl id
                session['empl_id'] = search_form.empl_id.data
                empl_id = search_form.empl_id.data

                #search students table for this student

                student = students.query.filter_by(empl_id = empl_id).first()

                #if a match is found
                if(student):
                    #create a new session list with student information
                    session['student_info'] = {'empl_id': empl_id,'students_id': student.id, 'first': student.first, 'last': student.last}


                    if(student.courses):
                        #student courses in a list of objects format
                        student_courses_objects = student.courses
                        print(student_courses_objects)
                        #loop through student courses creating a list with entries: courses_id, print string
                        #print string is text displayed in form
                        student_courses = []

                        for this_course in student_courses_objects:

                            #if an instructor is listed
                            if this_course.instructor:
                                instructor = this_course.instructor
                            else:
                                instructor = "NA"

                            print_string = this_course.subject + " " + str(this_course.catalog_num) + " Section: " + this_course.section + " Instructor: " + instructor
                            class_id = this_course.id

                            #add this course to courses list
                            student_courses.append([ class_id, print_string])

                        #add an option for not selecting a course
                        student_courses.append([0,"Not Available"])
                        session['student_courses'] = student_courses




                #No match for this empl id found
                else:
                    flash("No student with ID: " + session['empl_id'] + " found."  )
                    #clear session ID
                    session['empl_id'] = None

            #No Empl ID was entered
            else:
                flash("No Employee ID entered")

            #refresh page
            return redirect(url_for('register'))



        #signing a student in
        if 'sign_in_submitted' in request.form:
            print("SIGN IN FORM VALIDATED")
            #get student info from session variable
            student_info = session.get('student_info')

            if student_info != None:

                #create a sign in object with form data
                this_datetime = str(sign_in_form.date.data);
                this_datetime_split = this_datetime.split(" ")

                date = this_datetime_split[0]
                print(this_datetime_split[0])
                time = this_datetime_split[1]

                this_sign_in = sign_ins(students_id= student_info['students_id'], empl_id = student_info['empl_id'], purpose_id = sign_in_form.purpose_choice.data, courses_id = sign_in_form.student_courses.data , date = date, time = time )

                #add sign in to database
                db.session.add(this_sign_in)
                db.session.commit()

                #clear student data
                session['empl_id'] = None
                session['student_info'] = None
                session['student_courses'] = None

                flash("Student Successfully Added")
            else:
                flash("No student found to sign in")

            return redirect(url_for('register'))


        #render HTML template
        return render_template('register.html', search_form=search_form, sign_in_form = sign_in_form, student_info = session.get('student_info'))
    else:
        return render_template('login.html', login_form = login_form)


#This page is by instructors to check tutoring attendance. 
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    attendance_form = AttendanceForm()

    sign_in_list = []
    course = courses()

    if 'attendance_form_submitted' in request.form:

        pin = attendance_form.pin.data

        #this shows all sign ins
        if pin == login_password:
            sign_in_list = sign_ins.query;
            course.instructor = "All";
        else:
            pins_data = pins.query.filter_by(pin = pin).first()

            if(pins_data):
                course = pins_data.course
                sign_in_list = course.sign_ins
            else:
                flash("Incorrect Pin")


    return render_template('attendance.html', attendance_form = attendance_form, sign_in_list = sign_in_list, course = course)


if __name__ == '__main__':
    app.run(debug=True)
    manager.run()
