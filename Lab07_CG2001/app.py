from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db) #added flask migrate so that i could alter the db to include first/last name since i forgot to include those at the start. Learned to use it here. https://flask-migrate.readthedocs.io/en/latest/

class User(db.Model):#creating a user profile in the database.
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False, default='N/A')
    last_name = db.Column(db.String(20), nullable=False, default='N/A')
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    
def check_password(password):#make sure the password follows the format from previous lab.
    lowercase = any(char.islower() for char in password)
    uppercase = any(char.isupper() for char in password)
    ending_is_number = password[-1].isdigit()
    length = len(password) >= 8

    if lowercase and uppercase and ending_is_number and length:
        return True
    else:
        return False

@app.route('/', methods=['GET', 'POST'])
def signin():#sign in to the website.
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in the database.
        with app.app_context():
            user = User.query.filter_by(email=email, password=password).first()

        if user:
            return redirect(url_for('secret_page'))
        else:
            flash('Incorrect email or password.', 'danger')#flash messaging to alert the user of any errors. Learned from here https://flask.palletsprojects.com/en/2.3.x/patterns/flashing/
            return redirect(url_for('signin'))

    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Extracting form data.
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Checks to see if the email already exists in the database.
        with app.app_context():
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('This email has already been used.', 'danger')
            else:
                if password != confirm_password:  # Check if passwords match
                    flash('Passwords do not match.', 'danger')
                elif not check_password(password):  # Check password format
                    flash('Password must contain: A lowercase letter, An uppercase letter, 8 characters minimum, and end in a number.', 'danger')
                else:
                    # Save the user to the database
                    new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect(url_for('thank_you'))

    return render_template('signup.html')

@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')

@app.route('/secret')
def secret_page():
    return "This is the secret page. You have signed in successfully."

with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)