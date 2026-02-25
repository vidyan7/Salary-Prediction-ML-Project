from flask import Flask,render_template,request,redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os


app=Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB and Login manager
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#step1: load all the saved model
import pickle
with open("models/salary_rf_model.pkl","rb")as f:
    rf_model=pickle.load(f)
with open("models/lb_Job_Title.pkl","rb")as f:
    lb_Job_Title=pickle.load(f)

#step2: defining the function
def predict_salary(age=34.0,Gender='Male',Education_Level='PhD',Job_Title='Senior Data Engineer',Years_of_Experience=5.0):
    lst=[]
    lst=lst+[age]
    if Gender=="Female":
        lst=lst+[0]
    elif Gender=="Male":
        lst=lst+[1]
    elif Gender=="Other":
        lst=lst+[2]

    if Education_Level=="High School":
        lst=lst+[0]
    elif Education_Level=="Bachelor's Degree":
        lst=lst+[1]
    elif Education_Level=="Master's Degree":
        lst=lst+[2]
    elif Education_Level=="PhD":
        lst=lst+[3]

    Job_Title=lb_Job_Title.transform([Job_Title])
    lst=lst+list(Job_Title)

    lst=lst+[Years_of_Experience]
    print(lst)
    result=rf_model.predict([lst])
    return result[0]
    




@app.route('/')
@login_required
def index():
    return render_template('index.html')


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered.', 'warning')
            return redirect(url_for('register'))

        # Create new user
        new_user = User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
            
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))





@app.route('/predict',methods=['GET','POST'])
@login_required
def predict():
    if request.method=='POST':
        age=int(request.form.get('age'))
        Gender=request.form.get('Gender')
        Education_Level=request.form.get('Education_Level')
        Job_Title=request.form.get('Job_Title')
        Years_of_Experience=int(request.form.get('Years_of_Experience'))
        print(age,Gender,Education_Level,Job_Title,Years_of_Experience)



        result=predict_salary(age,Gender,Education_Level,Job_Title,Years_of_Experience)
        print(result)

        return render_template('predict.html', prediction=result)
    return render_template('predict.html')



if __name__=='__main__':
    with app.app_context():
        if not os.path.exists('users.db'):
            db.create_all()
    app.run(debug=True)