from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/feedback'  #FEEDBACK IS THE DB
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yfahgkszqqalhk:d33cf72af845039c0f0ec4dd3d5cbb8bd56c0d375f6460890aa6885802367da0@ec2-52-86-33-50.compute-1.amazonaws.com:5432/d5ll42nbull0gm' #production 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # to get warning

db = SQLAlchemy(app)    #db object pass in app to query db

#to create model in form of class and extend db model
class feedbacktable1(db.Model):
    __tablename__ = 'feedbacktable'
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.String(200), unique=True)
    professor = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    #class needs constructor or initializer 
    def __init__(self, student, professor, rating, comments):
        self.student = student
        self.professor = professor
        self.rating = rating
        self.comments = comments

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        student = request.form['student']
        professor = request.form['Professor']
        rating = request.form['rating']
        comments = request.form['comments']
       # print(student, professor, rating, comments)
        if student == '' or professor == '': #IF EMPTY
              return render_template('index.html', message='Please enter required fields')
        if db.session.query(feedbacktable1).filter(feedbacktable1.student == student).count() == 0:   #CHECKING DUPLICATE  #FEEDBACKTABLE1 IS CLASS NAME
            data = feedbacktable1(student, professor, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(student, professor, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')
if __name__ == '__main__':
	    app.run()	