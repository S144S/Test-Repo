from flask import Flask, render_template, url_for, redirect, request, jsonify, abort
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Users, Contents, Rewards
from forms import *
from flask_bcrypt import Bcrypt
import json
from datetime import datetime
import jdatetime

# Initializing the app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.debug = True
app.config['SECRET_KEY'] = 'FarzanSchool'

# Initializing the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Initializing the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# Register page
@app.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        is_admin = False
        user_name = form.user_name.data
        fname = form.first_name.data
        lname = form.last_name.data
        grade = form.grade.data
        password = form.password.data
        hashed_pass = bcrypt.generate_password_hash(password)
        print(type(user_name), type(fname))
        if('saeed144' in user_name):
            is_admin = True

        user = Users.query.filter_by(user_name=user_name).first()
        if not user:
            new_user = Users(user_name=user_name, password=hashed_pass, fname=fname,
            lname=lname, is_admin=is_admin, grade=grade)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)

# Login page
@app.route('/login', methods=('GET', 'POST'))
def login():
    # Already logged user does not need to login page
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data
        user = Users.query.filter_by(user_name=user_name).first()

        if user:
            check_pass = bcrypt.check_password_hash(user.password, password)
            if check_pass:
                login_user(user, remember=form.remember_me.data)
                user.last_login = datetime.utcnow()
                db.session.commit()
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))

    return render_template('login.html', form=form)

# Logout page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Landing page
@app.route('/')
@app.route('/landing')
def landing():
    user = ''
    if current_user.is_authenticated:
        user = current_user
        return redirect(url_for('home'))
    print(user)
    return render_template('index.html', user=user)

# Home page
@app.route('/home')
@login_required
def home():
    user = current_user
    return render_template('home.html', user=user)

# Getting content info
@app.route('/get-content-info', methods=["POST"])
@login_required
def get_content_info():
    data = request.get_json()
    if(data['grade'] < 10):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

# Course page
@app.route('/course')
@login_required
def course():
    user=current_user
    user_id = request.args.get('user_id')
    grade = request.args.get('grade')
    lesson = request.args.get('lesson')
    session = request.args.get('session')
    content = Contents.query.filter(Contents.grade==grade).filter(Contents.lesson == lesson).filter(Contents.session == session).first()

    if not content:
        return redirect(url_for('home', sit=1))

    script = content.script
    video = content.video
    deaf = content.deaf
    tabs = json.loads(content.tabs_content)
    quiz = json.loads(content.quiz)

    return render_template(
        'course.html',
        user=user,
        script=script,
        video=video,
        deaf=deaf,
        tabs=tabs,
        quiz=quiz
    )

# Adding course
@app.route('/add-course', methods=('GET', 'POST'))
@login_required
def add_course():
    if not current_user.is_admin:
        abort(404, 'Resource not found')
    form = AddCourseForm()
    if form.validate_on_submit():
        grade = form.grade.data
        lesson = form.lesson.data
        session = form.session.data
        script = form.script.data
        video = form.video.data
        deaf = form.deaf.data

        sec1 = form.sec1.data
        sec1_list = sec1.split('-')
        sec2 = form.sec2.data
        sec2_list = sec2.split('-')
        sec3 = form.sec3.data
        sec3_list = sec3.split('-')

        q1 = form.q1.data
        q1_list = q1.split('-')
        q1_list[-1] = int(q1_list[-1])
        q1_list[-2] = eval(q1_list[-2])
        q2 = form.q2.data
        q2_list = q2.split('-')
        q2_list[-1] = int(q2_list[-1])
        q2_list[-2] = eval(q2_list[-2])
        q3 = form.q3.data
        q3_list = q3.split('-')
        q3_list[-1] = int(q3_list[-1])
        q3_list[-2] = eval(q3_list[-2])
        q4 = form.q4.data
        q4_list = q4.split('-')
        q4_list[-1] = int(q4_list[-1])
        q4_list[-2] = eval(q4_list[-2])
        q5 = form.q5.data
        q5_list = q5.split('-')
        q5_list[-1] = int(q5_list[-1])
        q5_list[-2] = eval(q5_list[-2])

        quiz_dict = {
            'num': 5,
            1: q1_list,
            2: q2_list,
            3: q3_list,
            4: q4_list,
            5: q5_list,

        }
        quiz = json.dumps(quiz_dict)
        tabs_num = 3
        tabs_content_dict = {
            1: sec1_list,
            2: sec2_list,
            3: sec3_list
        }
        tabs_content = json.dumps(tabs_content_dict)
        new_content = Contents(
            grade=grade,
            lesson=lesson,
            session=session,
            script=script,
            video=video,
            deaf=deaf,
            quiz=quiz,
            tabs_num=tabs_num,
            tabs_content=tabs_content
        )
        try:
            db.session.add(new_content)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            print('faild')
    return render_template('add-course.html', user=current_user, form=form)

# Submit results
@app.route('/submit-result', methods=["POST"])
@login_required
def submit_result():
    data = request.get_json()
    user = Users.query.get(int(data['id']))
    activities = json.loads(user.activity)
    activity = [data['content'], data['res']]
    if not activities:
        activities.append(activity)
    else:
        for act in activities:
            if act[0] == data['content']:
                act[1] = data['res']
            else:
                activities.append(activity)

    user.activity = json.dumps(activities)
    db.session.commit()
    return jsonify({'success': True})

# Adding coupon
@app.route('/add-coupon', methods=('GET', 'POST'))
@login_required
def add_coupon():
    if not current_user.is_admin:
        abort(404, 'Resource not found')
    form = AddCouponForm()
    if form.validate_on_submit():
        code = form.code.data
        description = form.description.data
        expire_date = form.expire_date.data

        new_reward = Rewards(
            code = code,
            description=description,
            expire_date=expire_date
        )
        try:
            db.session.add(new_reward)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            print('faild')
    return render_template('add-coupon.html', user=current_user, form=form)

# Profile page
@app.route('/my-profile')
@login_required
def profile():
    user = Users.query.get(current_user.uid)
    form = UpdateUserForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        fname = form.first_name.data
        lname = form.last_name.data
        password = form.password.data
        hashed_pass = bcrypt.generate_password_hash(password)

        user.user_name = user_name
        user.fname = fname
        user.lname = lname
        user.password = hashed_pass
        db.session.commit()

        return redirect(url_for('logout'))
    
    activities = json.loads(user.activity)
    total_activity = len(activities)
    grade_A_cnt = 0
    grade_F_cnt = 0
    for activity in activities:
        if(activity[-1] == 2):
            grade_A_cnt += 1
        elif(activity[-1] == 0):
            grade_F_cnt += 1 
    last_login = jdatetime.datetime.fromgregorian(datetime=user.last_login).strftime('%Y/%m/%d')

    coupon = grade_A_cnt // 5
    remain_to_coupon = 5 - (grade_A_cnt % 5)

    rewards = []
    rewards_id = json.loads(user.reward_id)
    if rewards_id:
        i = 1
        for rid in rewards_id:
            reward = Rewards.query.get(rid)
            expire_date = jdatetime.datetime.fromgregorian(datetime=reward.expire_date).strftime('%Y/%m/%d')
            rewards.append([i, reward.code, reward.description, expire_date])
            i += 1


    return render_template(
        'profile.html',
        user=current_user,
        form=form,
        total_activity=total_activity,
        grade_A=grade_A_cnt,
        grade_F=grade_F_cnt,
        last_login=last_login,
        coupon=coupon,
        remain_to_coupon=remain_to_coupon,
        rewards=rewards
    )

# About us page
@app.route('/about-us')
@login_required
def about_us():
    return render_template('about.html', user=current_user)

# Contatct us page
@app.route('/contact-us')
@login_required
def contact_us():
    return render_template('contact.html', user=current_user)

# Start the app
if __name__ == '__main__':
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    app.run()