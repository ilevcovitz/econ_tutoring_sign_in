# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 12:43:53 2015

@author: Ivan
"""
import csv
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask.ext.script import Manager
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET KEY HERE'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hunterecon:mySQL_PASSWORD@hunterecon.mysql.pythonanywhere-services.com/hunterecon$econtutoring'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
moment = Moment(app)
db = SQLAlchemy(app)

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




db_sign_ins = sign_ins.query.all()

date = datetime.now().date()
time = datetime.now().time()

with open('/home/hunterecon/mysite/scripts/sign_in_exports/latest_export.csv','wt') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

    spamwriter.writerow(['Sign In ID'] + ['Date'] + ['Time'] + ['Employee ID'] + ['Purpose'] +  ['Last'] + ['First']  + ['Email'] + ['Subject'] + ['Catalog Num'] + ['Section'] + ['Instructor'] + ['Course Code'] + ['Term'])
    for sign_in in db_sign_ins:
        if sign_in.courses_id:
            spamwriter.writerow([sign_in.id] + [sign_in.date] + [sign_in.time] + [sign_in.empl_id] + [sign_in.purposes.purpose] + [sign_in.students.last] + [sign_in.students.first] + [sign_in.students.email] + [sign_in.courses.subject] + [sign_in.courses.catalog_num] + [sign_in.courses.section] + [sign_in.courses.instructor] + [sign_in.courses.code] + [sign_in.courses.term])
        else:
            spamwriter.writerow([sign_in.id] + [sign_in.date] + [sign_in.time] + [sign_in.empl_id] + [sign_in.purposes.purpose] + [sign_in.students.last] + [sign_in.students.first] + [sign_in.students.email] )


#export sign ins by course
#db_courses = courses.query.all()

#for course in db_courses:
 #   with open('/home/hunterecon/mysite/scripts/sign_in_by_course/' + str(course.catalog_num) + '_' + str(course.section) + '.csv','wt') as csvfile:
  #      spamwriter = csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
   #     spamwriter.writerow( ['Date']  + ['Purpose'] + ['Empl ID'] +  ['Last'] + ['First']   )
#
 #       for sign_in in course.sign_ins:
  #                  spamwriter.writerow( [sign_in.date] + [sign_in.purposes.purpose] + [sign_in.empl_id] + [sign_in.students.last] + [sign_in.students.first] )





