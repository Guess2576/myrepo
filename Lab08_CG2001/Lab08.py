
#Can be run using the pre-existing database file included in the instance folder. 
#I used flask and SQLAlchemy because I ran into issues using CGI that I could not resolve. 

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_database.db'
db = SQLAlchemy(app)

class Student(db.Model): #creating the database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    midterm_exam1 = db.Column(db.Float, nullable=False)
    midterm_exam2 = db.Column(db.Float, nullable=False)
    final_exam = db.Column(db.Float, nullable=False)

    @property
    def average_score(self): #taking average of ints from database
        return (self.midterm_exam1 + self.midterm_exam2 + 2 * self.final_exam) / 4

with app.app_context():
    db.create_all()

@app.route('/') #Displays student database.
def show_data():
    students = Student.query.all()
    return render_template('show_data.html', students=students)

@app.route('/enter_data', methods=['GET', 'POST']) #entering of data to be added to the table
def enter_data():
    if request.method == 'POST':
        name = request.form['name']
        midterm_exam1 = float(request.form['midterm_exam1'])
        midterm_exam2 = float(request.form['midterm_exam2'])
        final_exam = float(request.form['final_exam'])

        new_student = Student(name=name, midterm_exam1=midterm_exam1, midterm_exam2=midterm_exam2, final_exam=final_exam) #creates new entry in the DB.
        db.session.add(new_student)
        db.session.commit()
        return redirect('/')
    return render_template('enter_data.html')

@app.route('/delete', methods=['GET', 'POST']) #deletion of the data in the table
def delete_data():
    if request.method == 'POST':
        name = request.form['name']

        student_to_delete = Student.query.filter_by(name=name).first() #uses student name to delete the data associated with it.
        if student_to_delete:
            db.session.delete(student_to_delete)
            db.session.commit()
        return redirect('/')
    return render_template('delete_data.html')

if __name__ == '__main__':
    app.run(debug=True)