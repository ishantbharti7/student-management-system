


# changes/=login code update_password,update_password.html,login.html(flash message),navbars,admin register page,flash mesages demo,photo register done by admin code+html page change ,hod nav+hod_homepage.html added




from operator import and_
from flask import Flask, request, render_template, flash,url_for,redirect,session,send_from_directory, send_file,current_app,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from mimetypes import guess_type

app = Flask(__name__)
app.config['uploads'] = 'uploads' # set the upload folder path
bcrypt = Bcrypt(app)
app.config['uploads'] = 'uploads'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
app.config["SECRET_KEY"] = "fhshcsjndsnknnaxbkvhkdh"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/students'
db = SQLAlchemy(app)


class Notification(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(200))
    imagename = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    extend_existing=True

class AssignmentMarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rollno = db.Column(db.String(20))
    classs = db.Column(db.String(20))
    year = db.Column(db.Integer)
    assignment_title = db.Column(db.String(100))
    marks = db.Column(db.Integer)
    

    def __repr__(self):
        return f"AssignmentMarks('{self.roll_no}', '{self.class_name}', '{self.year}', '{self.assignment_title}', '{self.marks}')"

class logindata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    role = db.Column(db.Integer)
  

# class teacher(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(255), unique=True)
#     password = db.Column(db.String(255))
#     name = db.Column(db.String(255))
#     role = db.Column(db.Integer)
    
    
class Teacher(db.Model):
    def is_active(self):
        return True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    department = db.Column(db.String(100))
    role = db.Column(db.Integer())
    
    designation = db.Column(db.String(100))
    profile_picture = db.Column(db.String(100))
    password = db.Column(db.String(100))
    
class HOD(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    role = db.Column(db.Integer)
    
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    role = db.Column(db.Integer)
    
# class Assignment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=True)
#     duration = db.Column(db.Integer, nullable=False)
#     filename = db.Column(db.String(100), nullable=True)
#     classs = db.Column(db.String(100), nullable=True)
#     data = db.Column(db.LargeBinary, nullable=True)
    
class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    duration = db.Column(db.Integer, nullable=False)
    filename = db.Column(db.String(100), nullable=True)
    classs = db.Column(db.String(100), nullable=True)
    data = db.Column(db.LargeBinary, nullable=True)
    email = db.Column(db.String(100), nullable=False)  # Add email column
    
    submits = db.relationship('Assignment_submit', backref='assignment', lazy=True)

class Assignment_submit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    name=db.Column(db.String(20),nullable=False)
    title=db.Column(db.String(20),nullable=False)
    rollno=db.Column(db.Integer,nullable=False)
    classs=db.Column(db.String(30),nullable=False)
    submit_date=db.Column(db.DateTime, default=datetime.utcnow)
    upload_assignment = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=False)  # Add email column


class Records(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # email = db.Column(db.String(100))
    rollno = db.Column(db.String(100))
    classs = db.Column(db.String(100))
    subject = db.Column(db.String(100))
    year = db.Column(db.String(100))
    mst1 = db.Column(db.String(100))
    mst2 = db.Column(db.String(100))
    attendance = db.Column(db.String(100))

class Classs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100))
    classs = db.Column(db.String(54))
     
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    rollno = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(255))
    role = db.Column(db.Integer)
    classs = db.Column(db.String(255))
    section = db.Column(db.String(255))
    year = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    
    
class timetable_incharge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    role = db.Column(db.Integer)
 
class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(80))
    classs = db.Column(db.String(80))
    subject = db.Column(db.String(80))
    subject_code = db.Column(db.String(80),unique=False)
    semester = db.Column(db.String(80))
    teacher_name = db.Column(db.String(80))
    teacher_assigned_email = db.Column(db.String(80),db.ForeignKey('logindata.email'))
    day = db.Column(db.String(10))
    time = db.Column(db.String(10))   

class Attendance(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    rollno = db.Column(db.String(100), nullable=False)
    classs = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(100), nullable=False)
    month = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    attendance = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()




@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/admin')
def admin():
    if not session.get('admin_id'):
        return redirect('/login')
    return render_template('admin.html')


@app.route('/student_excel')
def upload_file():
    image_url = url_for('static', filename='images/demo.png')
    if not session.get('admin_id'):
        return redirect('/login')
    return render_template('upload.html', image_url=image_url)



@app.route('/upload', methods=['POST','GET'])
def upload():
    if not session.get('admin_id'):
        return redirect('/login')
    
    if 'file' not in request.files:
        return 'No file uploaded'
    else:
        file = request.files['file']
        file_name = file.filename
        file_data = file.read()
        df = pd.read_excel(file_data)
        df.columns = ['id', 'email', 'password', 'rollno', 'name', 'role', 'classs', 'semester', 'year']

        for _, row in df.iterrows():
            # check if email already exists in database
            if User.query.filter_by(email=row[2]).first() is not None:
                return f"Email {row[2]} already exists"
            else:
                # create new user and login data
                user = User(name=row[1],email=row[2],classs=row[3],password=row[4],rollno=row[5],role=row[6],semester=row[7],year=row[8])
                db.session.add(user)
                db.session.commit()
                login=logindata(name=row[1],email=row[2],password=row[4],role=row[6])
                db.session.add(login)
                db.session.commit()
        return 'File uploaded successfully!'




@app.route('/register', methods=['POST', 'GET'])
def register():
    email = ''
    if not session.get('admin_id'):
        return redirect('/login')
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        class_ = request.form.get('class')
        password = request.form.get('password')
        rollno = request.form.get('rollno')
        role = request.form.get('role')
        semester = request.form.get('semester')
        year = request.form.get('year')
        section=request.form.get('section')

        # Check if email already exists in the database
        existing_user = logindata.query.filter_by(email=email ).first()
        existing_rollno = User.query.filter_by(rollno=rollno).first()
        if existing_user:
            flash('Email or rollno already exists', 'danger')
            return render_template('register.html')
       
        if existing_rollno:
            
            flash('Rollno already exists', 'danger')
            return render_template('register.html')
    # else:
         # If email does not exist, proceed with registration
        user = User(email=email, password=password, section=section,rollno=rollno, role=role, name=name, classs=class_,
                    semester=semester, year=year)

        db.session.add(user)
        db.session.commit()
        user_for_login_data = logindata(email=email, password=password, role=role, name=name)
        db.session.add(user_for_login_data)
        db.session.commit()

        flash('New student added successfully', 'success')
        # return render_template('register.html')
    return render_template('register.html')

    

       





@app.route('/login/', methods=['POST','GET'])
def login():
  
    if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = logindata.query.filter_by(email=email).first()
           
            
            
            # Check if user exists in the database
            if user is None:
                flash('User not found. Please check your email and try again.','danger')
                return redirect('/login')
            
            # Check if password matches the hash stored in the database
            user_hash_password=check_password_hash(user.password, password)
            user_password=user.password==password
            if user and user_password:
                session['logged_in'] = True
                session['user_email'] = user.email
                flash('please change password first','success')
               
                return render_template('change_password.html')
            #  user_hash_password=check_password_hash(user.password, password)
            elif user and user_hash_password and user.role==1:
                session['logged_in']=True
                session['user_id']=user.email
                print(user.email)
                print(997999999999999999)
                print(user.role)
                print(session['user_id'])
                
                student = User.query.filter_by(email=session['user_id']).first()
                email = student.email
                name= student.name
                Rollno=student.rollno
                print(email)
                print(name)
                print(Rollno)
                print(student)
                print(user.role)
                
                return render_template('student_home.html',email=email,name=name,Rollno=Rollno)
                # return render_template('student_home.html')
            
            elif user and user_hash_password and user.role==2:
                session['logged_in']=True
                session['teacher_id']=user.email
                
                return redirect('/teacher')
            
            elif user and user_hash_password and user.role==3:
                session['logged_in']=True
                session['admin_id']=user.email
                # print(user.email)
                # print(9979999999999993948398999)
                return redirect('/admin')
            
            elif user and user_hash_password and user.role==4:
                session['logged_in']=True
                session['hod_id']=user.email
                return render_template('hod_homepage.html')
            
            elif user and user_hash_password and user.role==5:
                session['logged_in']=True
                session['timetableadmin_id']=user.email
                return redirect('/timetable_admin')
               
    return render_template('login.html')

@app.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    if 'logged_in' not in session:
        # user is not logged in, redirect to login page
        return redirect('/login')

    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Fetch the user from the database using their email
        user = logindata.query.filter_by(email=session['user_email']).first()

        if not user:
            # user not found in database
            raise Exception('User not found in database')

        # Check if the old password is correct
        if not (user.password, old_password):
            flash('Old password is incorrect.')
            return redirect('/change_password')

        # Check if the new password and confirm password match
        if new_password != confirm_password:
            flash('Passwords do not match.')
            return redirect('/change_password')

        # Hash the new password using bcrypt
        hashed_password = generate_password_hash(new_password)

        # Update the user's password in the database
        user.password = hashed_password
        db.session.commit()

        flash('Password updated successfully.','success')
        return redirect('/login')

    return render_template('change_password.html')
# update password

# @app.route('/update_password/', methods=['GET', 'POST'])
# def update_password():
#     if not session.get('user_id' ):
#         return redirect('/login')

#     if request.method == 'POST':
#         email = request.form.get('email')
#         old_password = request.form.get('old_password')
#         new_password = request.form.get('new_password')
#         confirm_password = request.form.get('confirm_password')

#         # Check if old password is correct
#         user = logindata.query.filter_by(email=email).first()
#         if user and check_password_hash(user.password, old_password):
#             if new_password == confirm_password:
#                 # Update password
#                 user.password = generate_password_hash(new_password)
#                 db.session.commit()
#                 flash('Password updated successfully', 'success')
#                 return redirect('/login')
#             else:
#                 flash('New password and confirm password do not match', 'danger')
#                 return render_template('update_password.html')
#         else:
#             flash('Old password is incorrect', 'danger')
#             return render_template('update_password.html')
#     else:
#         return render_template('update_password.html')



@app.route('/update_password/', methods=['GET', 'POST'])
def update_password():

    # Check if any user is logged in
    if not session.get('user_id') and not session.get('teacher_id') and not session.get('admin_id') and not session.get('hod_id') and not session.get('timetableadmin_id'):
        return redirect('/login')

    if request.method == 'POST':
        email = request.form.get('email')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Check if old password is correct
        user = logindata.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, old_password):
            if new_password == confirm_password:
                # Update password
                user.password = generate_password_hash(new_password)
                db.session.commit()
                flash('Password updated successfully', 'success')
                return redirect('/login')
            else:
                flash('New password and confirm password do not match', 'danger')
                return render_template('update_password.html')
        else:
            flash('Old password is incorrect', 'danger')
            return render_template('update_password.html')
    else:
        return render_template('update_password.html')

  


@app.route('/hod_homepage')
def hod_homepage():
    if not session.get('hod_id'):
        return redirect('/login')
    return redirect('/hod_homepage')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if not session.get('admin_id'):
        return redirect('/login')

    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        user = logindata.query.filter_by(email=email).first()
        if user:
            user.password = new_password
            db.session.commit()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('forgot_password'))
        else:
            flash('Invalid email', 'danger')
            return redirect(url_for('forgot_password'))
    else:
        return render_template('forgot_password.html')





# route for student home page
@app.route('/student_home')
def student_home():
    user_id = session.get('user_id')
    
   
    if not user_id:
        return redirect('/login')
    
    student = User.query.filter_by(email=session['user_id']).first()
    email = student.email
    name= student.name
    Rollno=student.rollno
    print(email)
    print(name)
    print(Rollno)
    print(student)
        # user = User.query.get(user_id)
      
    return render_template('student_home.html',email=email,name=name,Rollno=Rollno)




  
    
@app.route('/timetable_admin')
def timetable_admin():
    if not session.get('timetableadmin_id'):
        return redirect('/login')
    else:
        return render_template('/timetable_admin.html')







@app.route('/users')
def users():
    # Check if user is logged in
    if not session.get('admin_id'):
        return redirect('/login')

    # Query all users from the User model
    users = User.query.all()

    # Render the data in an HTML template
    return render_template('users.html', users=users)

@app.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    # Check if user is logged in
    if not session.get('admin_id'):
        return redirect('/login')

    # Query the user by ID from the User model
    user = User.query.get(user_id)

    if request.method == 'POST':
        # Update user data from form input
        user.email = request.form['email']
     
        user.rollno = request.form['rollno']
        user.name = request.form['name']
        user.role = request.form['role']
        user.classs = request.form['classs']
        user.year = request.form['year']
        user.semester = request.form['semester']

        # Commit changes to the database
        db.session.commit()

        return redirect('/users')

    # Render the edit user form
    return render_template('edit_user.html', user=user)

@app.route('/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Check if user is logged in
    if not session.get('admin_id'):
        return redirect('/login')

    # Query the user by ID from the User model
    user = User.query.get(user_id)

    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')





# Route to handle search requests
@app.route('/search', methods=['GET', 'POST'])
def search():
    if not session.get('admin_id'):
        return redirect('/login')

    if request.method == 'POST':
        search_option = request.form['search_option']
        search_value = request.form['search_value']
        users = None

        if search_option == 'email':
            users = User.query.filter_by(email=search_value).all()
        elif search_option == 'rollno':
            users = User.query.filter_by(rollno=search_value).all()
        elif search_option == 'name':
            users = User.query.filter_by(name=search_value).all()
        elif search_option == 'classs':
            users = User.query.filter_by(classs=search_value).all()
        elif search_option == 'year':
            users = User.query.filter_by(year=search_value).all()
        elif search_option == 'semester':
            users = User.query.filter_by(semester=search_value).all()

        return render_template('search.html', users=users)
    else:
        # Render the search form for GET requests
        return render_template('search.html')

    
    
    


@app.route('/register_teacher/', methods=['GET', 'POST'])
def teacher_register():
    if not session.get('admin_id'):
        return redirect('/login')

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        roles = request.form.get('role')
        existing_user = logindata.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists', 'danger')
            # return 'email already exist'
        else:
            # create instance of login data
            new_login = logindata(role=roles, email=email, password=password, name=name)
            db.session.add(new_login)
            db.session.commit()

            # check role and add to the appropriate table
            if roles == '2':
                new_teacher = Teacher(email=email, password=password, name=name,role=roles)
                db.session.add(new_teacher)
                db.session.commit()
            elif roles == '4':
                new_hod = HOD(email=email, password=password, name=name,role=roles)
                db.session.add(new_hod)
                db.session.commit()
            elif roles == '5':
                new_timetable_incharge = timetable_incharge(email=email, password=password, name=name,role=roles)
                db.session.add(new_timetable_incharge)
                db.session.commit()
                
            elif roles == '3':
                new_admin = Admin(email=email, password=password, name=name,role=roles)
                db.session.add(new_admin)
                db.session.commit()

            flash('Data entered successfully', 'success')
            return redirect('/register_teacher/')

    return render_template('register_teacher.html')



@app.route('/register_hod/', methods=['GET', 'POST'])
def register_hod():
    # Check if admin is logged in
    if not session.get('admin_id'):
        return redirect('/login')

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        existing_user = logindata.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists', 'danger')
            return 'email already exists'
        else:
            # Define and initialize the new_timetable variable
            new_timetable = HOD(email=email, password=password, name=name, role=role)
            db.session.add(new_timetable)
            db.session.commit()

            TT_for_login_data = logindata(email=email, password=password, role=role, name=name)
            db.session.add(TT_for_login_data)
            db.session.commit()

            return "done"

    return render_template('register_hod.html')

    


# REGISTER AS TIMETABLE
@app.route('/timetable_incharge/',methods=['GET','POST'])
def timetable_register():
    # Check if admin is logged in
    if not session.get('timetableadmin_id'):
        return redirect('/login')
    
    if request.method=='POST':
        
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        existing_user =logindata.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists', 'danger')
            return 'email already exist'
        else:
            # Define and initialize the new_timetable variable
            new_timetable=timetable_incharge(email=email,password=password,name=name,role=role)
            db.session.add(new_timetable) 
            db.session.commit()
            
            TT_for_login_data=logindata(email=email,password=password,role=role,name=name)
            db.session.add(TT_for_login_data)
            db.session.commit()
         
            return "done"
    
    return render_template('timetable_incharge.html')




@app.route('/display_teachers', methods=['GET', 'POST'])
def display_teachers():
    # Check if admin is logged in
    if not session.get('admin_id'):
        return redirect('/login')

    # Get the search query from the form
    search_query = request.form.get('search_query')

    # Query the users where role is equal to 2 from the logindata model
    users = logindata.query.filter_by(role=2).all()

    # Filter users based on search query
    if search_query:
        users = [user for user in users if search_query in user.name]

    # Render the users in an HTML page with search bar
    return render_template('display_teachers.html', users=users, search_query=search_query)


# Route to handle search queries
@app.route('/search_teachers', methods=['GET'])
def search_teachers():
    # Check if admin is logged in
    if not session.get('admin_id'):
        return redirect('/login')

    # Get the query parameter from the URL
    search_query = request.args.get('query')

    # Query the users where role is equal to 2 from the logindata model
    users = logindata.query.filter_by(role=2).all()

    # Filter users based on search query
    if search_query:
        users = [user for user in users if search_query in user.name]

    # Render the users in an HTML page with search bar
    return render_template('display_teachers.html', users=users, search_query=search_query)



@app.route('/logindata/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_teacher(user_id):
    # Check if admin is logged in
    if not session.get('admin_id'):
        return redirect('/login')

    # Query the user by ID from the User model
    user = logindata.query.get(user_id)

    if request.method == 'POST':
        # Update user data from form input
        user.email = request.form['email']
        user.name = request.form['name']

        # Commit changes to the database
        db.session.commit()

        return redirect('/display_teachers')

    # Render the edit user form
    return render_template('edit_teacher.html', user=user)


@app.route('/logindata/delete/<int:user_id>', methods=['POST'])
def delete_teacher(user_id):
    # Check if admin is logged in
    if not session.get('admin_id'):
        return redirect('/login')

    # Query the user by ID from the User model
    user = logindata.query.get(user_id)

    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()

    return redirect('/display_teachers')





@app.route('/display_t')
def display_t():
    # Check if admin is logged in
    if not session.get('admin_id'):
        return redirect('/login')

    timetable_incharge_data = timetable_incharge.query.all()
    return render_template('display_t.html', timetable_incharge_data=timetable_incharge_data)


@app.route('/timetable_incharge/delete/<int:id>', methods=['POST'])
def delete_timetable_incharge(id):
    # Check if admin is logged in
    if not session.get('admin_id'):
        return redirect('/login')

    if request.method == 'POST':
        # Logic for deleting user from database based on ID
        user = timetable_incharge.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return redirect('/display_t')  # Redirect to display_users page after deletion
    

    



@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    if not session.get('teacher_id'):
        return redirect('/login')
    
    email = session.get('teacher_id')
    user = Teacher.query.filter_by(email=email).first()
    users = Timetable.query.filter_by(teacher_assigned_email=email).all()
    
    return render_template('teacher.html', user=user, users=users)

@app.route('/update', methods=['GET','POST'])
def update():
    email = session.get('teacher_id')
    teacher = Teacher.query.filter_by(email=email).first()
    if teacher:
        teacher.name = request.form['name']
        teacher.email = request.form['email']
        teacher.department = request.form['department']
        teacher.designation = request.form['designation']
        # Handle profile_picture upload
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file.filename != '': 
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['uploads'], filename))
                teacher.profile_picture = filename
        db.session.commit()
        flash('Profile updated successfully', 'success')
    return redirect(url_for('teacher'))

@app.route('/add_attendance', methods=['POST'])
def add_attendance():
    classs = request.form.get('classs')
    year = request.form.get('year')
    for student in User.query.filter_by(classs=classs, year=year).all():
        rollno = student.rollno
        year = student.year
        mst1 = request.form.get('mst1_' + str(rollno))
        mst2 = request.form.get('mst2_' + str(rollno))
        attendance = request.form.get('attendance_' + str(rollno))
        subject = request.form.get('subject_' + str(rollno))
        attendance_record = Records.query.filter_by(rollno=rollno, classs=classs).first()
        if attendance_record and attendance_record.subject == subject:
            attendance_record.mst1 = mst1
            attendance_record.mst2 = mst2
            attendance_record.attendance = attendance
            db.session.commit()
        else:
            attendance_record = Records(subject=subject,rollno=rollno,year=year, classs=classs, mst1=mst1, mst2=mst2, attendance=attendance)
            db.session.add(attendance_record)
            db.session.commit()
    return redirect('/attendance_record')
from flask import Flask, request, render_template
import pandas as pd


@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        csv_file = request.files['file']
        if csv_file.filename.endswith('.csv'):
            df = pd.read_csv(csv_file.stream)
            classs = request.form.get('classs')
            year = request.form.get('year')
            subject = request.form.get('subject')
            if not classs:
                return "Please select a class"
            for index, row in df.iterrows():
                rollno = row['rollno']
                if User.query.filter_by(classs=classs, year=year, rollno=rollno).count() == 1:
                    mst1 = row['mst1']
                    mst2 = row['mst2']
                    attendance = row['attendance']
                    attendance_record = Records.query.filter_by(rollno=rollno, classs=classs).first()
                    if attendance_record and attendance_record.subject == subject:
                        attendance_record.mst1 = mst1
                        attendance_record.mst2 = mst2
                        attendance_record.attendance = attendance
                        db.session.commit()
                    else:
                        attendance_record = Records(subject=subject,rollno=rollno,year=year, classs=classs, mst1=mst1, mst2=mst2, attendance=attendance)
                        db.session.add(attendance_record)
                        db.session.commit()
            return redirect('/attendance_record')
        else:
            return "Please upload a valid CSV file"
    else:
        return render_template('attendance_record.html')



@app.route('/attendance_record')
def attendance_record():
    records = Records.query.all()
    return render_template('attendance_record.html', records=records)

@app.route('/edit_record/<int:id>', methods=['GET', 'POST'])
def edit_record(id):
    record = Records.query.get(id)
    if request.method == 'POST':
        record.mst1 = request.form['mst1']
        record.mst2 = request.form['mst2']
        record.attendance = request.form['attendance']
        db.session.commit()
        flash('Record updated successfully!', 'success')
        return redirect(url_for('attendance_record'))
    return render_template('edit_record.html', record=record)


    
@app.route('/delete_record/<int:id>', methods=['POST'])
def delete_record(id):
    record = Records.query.get(id)
    db.session.delete(record)
    db.session.commit()
    flash('Record deleted successfully!', 'success')
    return redirect(url_for('attendance_record'))

@app.route('/search_student', methods=['GET', 'POST'])
def search_student():
    if request.method == 'POST':
        classs = request.form.get('class')
        year = request.form.get('year')
        subject = request.form.get('subject')
        if not classs:
            return "Please select a class"
        students = User.query.filter_by(classs=classs, year=year).all()
        records = db.session.query(User, Records).\
          outerjoin(Records, and_(User.classs == Records.classs, User.rollno == Records.rollno)).\
          filter(User.classs == classs, User.year == year).all()
    else:
        students = []
        records = []
        classs = None
        year = None
        subject = None
    return render_template('search_student.html', classs=classs, year=year, subject=subject, students=students, records=records)

import os
from flask import render_template, request, redirect, url_for


@app.route('/notifications/add', methods=['GET', 'POST'])
def add_notifications():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files.get('file')
        # image = request.files.get('image')

        # Check if a file was uploaded
        if file:
            filename = os.path.join(app.config['uploads'], file.filename)
            file.save(filename)
        else:
            filename = None



        # Create a new Notification object
        notification = Notification(title=title, description=description,
                                     filename=filename)

        # Save the new Notification object to the database
        db.session.add(notification)
        db.session.commit()

        return redirect(url_for('teacher'))

    return render_template('add_notifications.html') 

@app.route('/view_notifications')
def view_notifications():
    notification = Notification.query.all()
    return render_template('view_notifications.html', notification=notification)

@app.route('/notifications/edit/<int:id>', methods=['GET', 'POST'])
def edit_notifications(id):
    notification = Notification.query.get_or_404(id)

    if request.method == 'POST':
        notification.title = request.form['title']
        notification.description = request.form['description']
        file = request.files.get('file')
        # image = request.files.get('image')

        # Check if a new file was uploaded
        if file:
            filename = os.path.join(app.config['uploads'], file.filename)
            file.save(filename)
            notification.filename = filename



        # Update the Notification object in the database
        db.session.commit()

        return redirect(url_for('teacher'))

    return render_template('edit_notification.html', notification=notification)

    

    

@app.route('/notifications/delete/<int:id>', methods=['POST'])
def delete_notifications(id):
    notification = Notification.query.get_or_404(id)

    # Delete the Notification object from the database
    db.session.delete(notification)
    db.session.commit()

    return redirect(url_for('teacher'))





@app.route('/add_assignment', methods=['GET', 'POST'])
def add_assignment():
    if request.method == 'POST':
        email = session.get('teacher_id')
        
        title = request.form['title']
        duration = request.form['duration']
        content = request.form['content']
        classs = request.form['classs']
        file = request.files.get('file')
        data = b''
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['uploads'], filename)
            file.save(file_path)
            with open(file_path, 'rb') as f:
                data = f.read()
        else:
            filename = None

        if title and duration:
            assignment = Assignment(email=email,title=title, duration=duration, content=content, classs=classs, filename=filename,data=data)
            db.session.add(assignment)
            db.session.commit()

            return redirect(url_for('add_assignment'))

    return render_template('add_assignment.html')


@app.route('/nav_bar')
def nav_bar():
    return render_template('nav_bar.html')



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    if request.method == 'POST':
        assignment.title = request.form['title']
        assignment.duration = request.form['duration']
        assignment.content = request.form['content']
        assignment.classs = request.form['classs']
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            assignment.file_name = filename
        db.session.commit()
        # return redirect(url_for('view_assignment'))
    return render_template('edit_assignment.html', assignment=assignment)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_assignment(id):
    assignment = Assignment.query.filter_by(id=id).first()
    db.session.delete(assignment)
    db.session.commit()
    return redirect(url_for('view_assignments'))

@app.route('/view_assignment')
def view():
    assignments = Assignment.query.all()
    return render_template('view_assignment.html',assignments=assignments)




@app.route('/responses/')
def view_responses():
    email = session.get('teacher_id')
    assignments = db.session.query(Assignment_submit, AssignmentMarks)\
        .join(AssignmentMarks, and_(
            Assignment_submit.rollno == AssignmentMarks.rollno,
            Assignment_submit.title == AssignmentMarks.assignment_title,
        ))\
        .filter(Assignment_submit.email == email)\
        .all()
    return render_template('response.html', assignments=assignments)

@app.route('/add_marks', methods=['POST'])
def add_marks():
    assignment_id = request.form['id']
    marks = request.form['marks']
    
    # Retrieve the assignment from the database
    
    assignment = Assignment_submit.query.get_or_404(assignment_id)
    
    # Insert the marks into the AssignmentMarks table
    new_marks = AssignmentMarks(
        rollno=assignment.rollno,
        classs=assignment.classs,
        # year=assignment.year,
        assignment_title=assignment.title,
        marks=marks
    )
    db.session.add(new_marks)
    db.session.commit()
    
    flash('Marks added successfully.')
    return redirect(url_for('view_responses'))

@app.route('/download/<int:id>')
def download_file(id):
    assignment = Assignment_submit.query.get_or_404(id)
    notification = Notification.query.get_or_404(id)
    file_path = os.path.join(current_app.root_path, 'uploads', assignment.upload_assignment,notification.filename)

    return send_file(file_path, mimetype=guess_type(file_path)[0], as_attachment=True)
    


@app.route('/upload_timetable', methods=['POST'])
def upload_timetable():
    if not session.get('timetableadmin_id'):
        return redirect('/login')
    
    file = request.files['file']
    if file:
        # read the excel file into a pandas dataframe
        df = pd.read_excel(file)
        # loop through the rows of the dataframe and save each row as a new entry in the database
        for _, row in df.iterrows():
            timetable_entry = Timetable(
                department=row['Department'],
                classs=row['Classs'],
                subject=row['Subject'],
                subject_code=row['Subject Code'],
                semester=row['Semester'],
                teacher_name=row['Teacher Name'],
                teacher_assigned_email=row['Teacher Assigned Email'],
                day=row['Day'],
                time=row['Time']
            )
            db.session.add(timetable_entry)
        db.session.commit()
        return 'File uploaded successfully'
    return 'No file selected'


def allowed_file(filename):
    # Check if the file has allowed extension
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['xls', 'xlsx']
           

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    elif 'admin_id' in session:
        session.pop('admin_id')
    elif 'teacher_id' in session:
        session.pop('teacher_id')
    elif 'hod_id' in session:
        session.pop('hod_id')
    elif 'timetableadmin_id' in session:
        session.pop('timetableadmin_id')
    # session.clear()  # Clear all session data
    return redirect('/login')


@app.route('/student_upload', methods=['GET', 'POST'])
def add_assignment_upload_by_student():
    if not session.get('user_id'):
        return redirect('/login')

    # Get the user details based on the email stored in the session
    user = User.query.filter_by(email=session.get('user_id')).first()

    if request.method == 'POST':
        assignment_id = request.form.get('assignment_id')
        assignment = Assignment.query.get(assignment_id)
        # assignment = Assignment.query.get(title)
        name = user.name
        rollno = user.rollno
        classs = user.classs
        title = assignment.title
        email = assignment.email
        
        existing_submission = Assignment_submit.query.filter_by(assignment_id=assignment_id, rollno=rollno).first()

        if existing_submission:
            flash( 'You have already submitted a file for this assignment.',"success")
            return render_template('student_upload_assignment.html')

        file = request.files.get('upload_assignment')
        data = b''
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['uploads'], filename)
            file.save(file_path)
            data = filename
        else:
            filename = None

        if assignment_id and name and rollno and classs:
            assignment_submit = Assignment_submit(assignment=assignment,email=email, title=title, name=name, rollno=rollno, classs=classs, upload_assignment=data)
            db.session.add(assignment_submit)
            db.session.commit()
            flash('Assignment submitted sucessfully','success')
            return render_template('student_upload_assignment.html')

    assignments = Assignment.query.all()
    return render_template('student_upload_assignment.html', assignments=assignments)





@app.route('/student_assignments')
def student_assignments():
    if not session.get('user_id'):
        return redirect('/login')
    
    # Get the current user's rollno from the session
    student = User.query.filter_by(email=session['user_id']).first()
    rollno = student.rollno

    # Query all assignments
    assignments = Assignment.query.all()

    # Query all submitted assignments by the current user
    submitted_assignments = Assignment_submit.query.filter_by(rollno=rollno).all()

    # Create a list of submitted assignment ids
    submitted_assignment_ids = [assignment.assignment_id for assignment in submitted_assignments]

    # Render the student_assignments.html template with the assignments
    return render_template('student_assignment.html', assignments=assignments, submitted_assignment_ids=submitted_assignment_ids)

@app.route('/submitted_history')
def student_submit_history():
    if not  session.get('user_id'):
        return redirect('/login')
    student = User.query.filter_by(email=session['user_id']).first()
    rollno = student.rollno
    submitted_assignments = Assignment_submit.query.filter_by(rollno=rollno).all()
    uploaded_files = {}
    for submit in submitted_assignments:
        uploaded_files[submit.assignment_id] = submit.upload_assignment
        assignments = Assignment.query.all()
    return render_template('student_history.html', assignments=assignments, uploaded_files=uploaded_files)

    
@app.route('/download_assignments/<int:assignment_id>')
def download_assignment_history(assignment_id):
    if not session.get('user_id'):
        return redirect('/login')
    # Query the assignment with the specified ID from the database
    assignment = Assignment_submit.query.filter_by(id=assignment_id).first()
    # Check if the assignment exists
    if not assignment:
        flash('The requested assignment does not exist in db.')
        return redirect(url_for('student_assignments'))

    # Generate the file path to the assignment file
    file_path = os.path.join(current_app.root_path, 'uploads', assignment.upload_assignment)

    # Check if the assignment file exists
    if not os.path.exists(file_path):
        flash('The requested assignment file does not exist on disk.')
        return redirect(url_for('student_assignments'))

    # Return the file for download
    return send_file(file_path, mimetype=guess_type(file_path)[0], as_attachment=True)







@app.route('/download_assignment/<int:assignment_id>')
# @login_required
def download_assignment(assignment_id):
    if not session.get('user_id'):
        return redirect('/login')
    # Query the assignment with the specified ID from the database
    assignment = Assignment.query.filter_by(id=assignment_id).first()
    # Check if the assignment exists
    if not assignment:
        flash('The requested assignment does not exist in db.')
        return redirect(url_for('student_assignments'))

    # Generate the file path to the assignment file
    file_path = os.path.join(current_app.root_path, 'uploads', assignment.filename)

    # Check if the assignment file exists
    if not os.path.exists(file_path):
        flash('The requested assignment file does not exist on disk.')
        return redirect(url_for('student_assignments'))

    # Return the file for download
    return send_file(file_path, mimetype=guess_type(file_path)[0], as_attachment=True)





if __name__ == '__main__':
    app.run(debug=True)

# student role =1
# teacher role=2
# admin role=3
# hod role=4
# TT role=5