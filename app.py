from flask import Flask, render_template, url_for, redirect, request, jsonify, abort
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_migrate import Migrate
from models import db, Users, Groups, Islands, Helps, TextBooks
from forms import *
from flask_bcrypt import Bcrypt
import json
from datetime import datetime
import ast
import jdatetime
import random
import string
import os
from werkzeug.utils import secure_filename

# Initializing the app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.debug = True
app.config['SECRET_KEY'] = 'FarzanSchool'

# /static/img/profiles/
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])

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
        is_teacher = True
        user_name = form.user_name.data
        fname = form.first_name.data
        lname = form.last_name.data
        grade = form.grade.data
        password = form.password.data
        hashed_pass = bcrypt.generate_password_hash(password)
        if(('saeed144' in user_name) or ('island_admin' in user_name)):
            is_admin = True
        students = "[]"
        user = Users.query.filter_by(user_name=user_name).first()
        if not user:
            new_teacher = Users(user_name=user_name, password=hashed_pass, fname=fname,
            lname=lname, is_admin=is_admin, grade=grade, students=students, is_teacher=is_teacher)
            db.session.add(new_teacher)
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
            hashed_pass = user.password
            check_pass = bcrypt.check_password_hash(hashed_pass, password)
            if check_pass:
                login_user(user, remember=form.remember_me.data)
                current_user.last_login = datetime.utcnow()
                db.session.commit()
                next_page = request.args.get('next')
                if user.is_teacher:
                    return redirect(next_page) if next_page else redirect(url_for('teacher'))
                return redirect(next_page) if next_page else redirect(url_for('group'))

    return render_template('login.html', form=form)

# Logout page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Home page
@app.route('/home')
@app.route('/')
def home():
    user = ''
    if current_user.is_authenticated:
        user = current_user
        if user.is_teacher:
            return redirect(url_for('teacher'))
        else:
            return redirect(url_for('group'))

    return render_template('index.html', user=user)

# Teacher page
@app.route('/teacher')
@login_required
def teacher():
    user = ''
    if current_user.is_authenticated:
        user = current_user

    if not current_user.is_teacher:
        return redirect(url_for('group'))
    
    groups = Groups.query.order_by(Groups.money).all()
    print(groups)
    return render_template('teacher.html', user=user, groups=groups)

# Students registration page
@app.route('/students-reg')
@login_required
def students_reg():
    user = ''
    if current_user.is_authenticated:
        user = current_user

    if not current_user.is_teacher:
        return redirect(url_for('group'))

    form = StudentsSetupForm()
    return render_template('student-registeration.html', form=form, user=user)

# Get students info API
@app.route('/get-students', methods=["POST"])
def get_students():
    if not current_user.is_teacher:
        return redirect(url_for('group'))
    data = request.get_json()

    students = data['students']
    class_name =  data['class']
    grade = int(data['grade'])
    students_num = int(data['quantity'])
    groups = int(data['groups'])
    defualt_pass = bcrypt.generate_password_hash(data['password'])

    # Add groups to DB
    for i in range(groups):
        group_name = class_name + '-' + str(grade) + '-'
        group_name += str(i+1)
        print('create group ', group_name)
        memebers = {}
        m = 1
        for member in students:
            if(int(member['group'])) == (i+1):
                memebers[m] = member['user_name']
                m += 1
        memebers = json.dumps(memebers)
        new_group = Groups(name=group_name, memebers=memebers)
        db.session.add(new_group)
        db.session.commit()
    
    # Get the teacher
    teacher = Users.query.get(current_user.uuid)
    teacher_students = ast.literal_eval(teacher.students)
    teacher_students_num = teacher.students_num
    student_cnt = 0
    # Add students to DB
    for student in students:
        group_name = class_name + '-' + str(grade) + '-'
        group_name += student['group']
        group = Groups.query.filter_by(name=group_name).first()

        fname = student['fname']
        lname = student['lname']
        user_name = student['user_name']
        group_id = group.guid

        new_student = Users(user_name=user_name, group_id=group_id, password=defualt_pass,
                                fname=fname, lname=lname, grade=grade)
        db.session.add(new_student)
        db.session.commit()
        # Add the student to the teacher
        student_cnt += 1
        teacher_students.append(new_student.uuid)
    
    # Update teacher instance
    teacher_students_num += student_cnt
    teacher.students_num = teacher_students_num
    teacher.students = str(teacher_students)
    db.session.commit()

    return jsonify({"success": True})

# Show students info page
@app.route('/show-students')
@login_required
def show_students():
    user = current_user

    if not current_user.is_teacher:
        return redirect(url_for('group'))
    
    teacher_students = ast.literal_eval(user.students)
    students_list = []
    for student in teacher_students:
        students_list.append(Users.query.get(student))
    
    teams = []
    for student in students_list:
        if student.group_id not in teams:
           teams.append(student.group_id) 

    groups = []
    
    for id in teams:
        groups.append(Groups.query.get(id))

    members = []
    island_name = []
    unclear_level = []
    hard_chalenges = []
    hard_chalenges_dic = {}
    for team in groups:
        members.append(json.loads(team.memebers))
        island_name.append(Islands.query.get(team.island).name)
        if team.just_pass:
            activity = json.loads(team.activity)
            info = []
            for act in activity:
                if act[-1] == 0:
                    name = Islands.query.get(act[0]).name
                    info.append([name, act[1]])
                    hard_chalenges.append([name, act[1]])
                    
            unclear_level.append(info)
        else:
            unclear_level.append([])

    for sublist in hard_chalenges:
        key = sublist[0]
        values = sublist[1:]
        if key in hard_chalenges_dic:
            hard_chalenges_dic[key].extend(values)
        else:
            hard_chalenges_dic[key] = values
    print(hard_chalenges_dic)
    return render_template(
        'show-students.html',
        user=user,
        students=students_list,
        groups=groups,
        members=members,
        island_name=island_name,
        unclear_level=unclear_level,
        hard_chalenges=hard_chalenges_dic
    )

# My group page
@app.route('/my-group')
@login_required
def group():
    avatars_name = [
        'nasir',
        'qias',
        'kharazmi',
        'mirzakhani',
        'behzad',
        'hashtroodi',
        'khayam',
        'vafa',
        'vesal',
        'yegane',
    ]

    user = ''
    if current_user.is_authenticated:
        user = current_user

    if current_user.is_teacher:
        redirect(url_for('teacher'))
    
    group = Groups.query.get(int(user.group_id))
    members = json.loads(group.memebers)
    members_name = []
    
    for member in members.values():
        print(member)
        ins = Users.query.filter_by(user_name=member).first()
        mn = ins.fname + ' ' + ins.lname
        members_name.append(mn)

    islands = Islands.query.filter_by(grade=user.grade).order_by(Islands.iuid).all()

    groups = Groups.query.all()
    for team in groups:
        if (team.guid != group.guid) and (team.school == group.school):

            if team.avatar in avatars_name:
                avatars_name.remove(team.avatar)
                
    return render_template('my-group.html',
                           user=user,
                           group=group,
                           members=members_name,
                           passed_islands=group.passed_islands,
                           avatars_name=avatars_name
            )

# Create island
@app.route('/create-island', methods=('GET', 'POST'))
@login_required
def create_island():
    form = CreateIslandForm()
    if form.validate_on_submit():
        name = form.name.data
        grade = form.grade.data
        lesson = form.lesson.data
        start_date = form.start_date.data
        deadline = form.end_date.data
        problems_dict = {
            1: [form.p1.data, form.a1.data],
            2: [form.p2.data, form.a2.data],
            3: [form.p3.data, form.a3.data],
            4: [form.p4.data, form.a4.data],
            5: [form.p5.data, form.a5.data],
            6: [form.p6.data, form.a6.data]
        }
        problems = json.dumps(problems_dict)
        text_book_dict = {
            1: [form.t1.data, 12],
            2: [form.t2.data, 25],
            3: [form.t3.data, 48]    
        }
        text_book = json.dumps(text_book_dict)
        treasure = form.treasure.data
        island_avatar = form.avatar.data
        island_map = form.map.data
        levels_coord = '{}'
        bio_dict = {
            1: [form.scientist.data, form.b1.data],
            2: [form.scientist.data, form.b2.data],
            3: [form.scientist.data, form.b3.data],
            4: [form.scientist.data, form.b4.data],
            5: [form.scientist.data, form.b5.data],
            6: [form.scientist.data, form.b6.data]
        }
        bio = json.dumps(bio_dict)
        try:
            new_island = Islands(
                name=name,
                grade=grade,
                problems=problems,
                text_book=text_book,
                treasure=treasure,
                start_date=start_date,
                deadline=deadline,
                island_avatar=island_avatar,
                island_map=island_map,
                levels_coord=levels_coord,
                bio=bio,
                lesson=lesson
            )
            db.session.add(new_island)
            db.session.commit()
            return redirect(url_for('teacher'))
        except:
            return render_template('create-island.html', user=current_user, form=form)
    return render_template('create-island.html', user=current_user, form=form)

# Add islands API
@app.route('/add-island')
@login_required
def add_island():
    if current_user.is_admin:
        name = 'خوارزمی'
        grade = 9
        problems_dict = {
            1: ["img/problems/isl91p1.jpg", 2],
            2: ["img/problems/isl91p1.jpg", 1],
            3: ["img/problems/isl91p1.jpg", 3],
            4: ["img/problems/isl91p1.jpg", 4],
            5: ["img/problems/isl91p1.jpg", 1],
            6: ["img/problems/isl91p1.jpg", 2],
        }
        problems = json.dumps(problems_dict)
        text_book_dict = {
            1: ["isl91t1.jpg", 12],
            2: ["isl91t2.jpg", 43]
        }
        text_book = json.dumps(text_book_dict)
        treasure = 5000
        deadline = datetime(2023, 2, 23, 17, 0, 0)
        island_avatar = 'img/islands-avatar/isl-def.jpg'
        island_map = 'isl-def.png'
        levels_coord_dict = {
            1: [514.71, 576.76, 34],
            2: [329.56, 583.37, 34],
            3: [168.11, 451.03, 34],
            4: [352.59, 367.53, 34],
            5: [505.87, 219.59, 34],
            6: [651.77, 285.82, 34],
        }
        levels_coord = json.dumps(levels_coord_dict)
        bio_dict = {
            1: ['isl91b1', 'جمشید بن مسعود بن محمود طبیب کاشانی ملقب به غیاث‌الدین (۷۵۸ ش ۱۳۸۰ م – ۱ تیر ۸۰۸ ش یا ۲۲ ژوئن م۱۴۲۹) ریاضی‌دان و اخترشناس ایرانی بود. او در غرب به الکاشی (al-kashi) مشهور است.'],
            2: ['', 'علاقهٔ اصلی وی متوجه ریاضیات و اخترشناسی بود و تحت حمایت الغ‌بیگ موقعیت شغلی مطمئنی در سمرقند داشت.'],
            3: ['', 'ابداع و ترویج کسرهای اعشاری به قیاس با کسرهای شصتگانی که در ستاره‌شناسی متداول بود. محاسبهٔ عدد پی تا شانزده رقم اعشار، به نحوی که تا صدوهشتاد سال بعد کسی نتوانست آن را گسترش دهد'],
            4: ['', 'کاشانی مقدار سینوس یک درجه را تا ده رقم صحیح شصتگانی حساب کرد.'],
            5: ['', 'کاشانی نخستین کسی بود که در اوائل قرن ۱۵ میلادی علامت اعشار را بکار برد. تا پیش از او اعداد غیر صحیح بصورت رقم صحیح بهمراه یک کسر نمایش داده می‌شدند.'],
            6: ['', 'کاشانی در الرسالة المُحیطیة (ص ۲۸) در سال ۱۴۲۴ میلادی با استفاده از یک ۸۰۵۳۰۶۳۶۸ (هشتصد و پنج میلیون) ضلعی عدد پی را تا ۱۶ رقم اعشار محاسبه کرد که رکورد او تا ۱۸۰ سال توسط هیچ ریاضیدانی شکسته نشد!']
        }
        bio = json.dumps(bio_dict)
        try:
            # isl = Islands.query.get(1)
            # isl.bio = bio
            # isl.text_book = text_book
            # isl.island_map = island_map
            # new_island = Islands(
            #     name=name,
            #     grade=grade,
            #     problems=problems,
            #     text_book=text_book,
            #     treasure=treasure,
            #     deadline=deadline,
            #     island_avatar=island_avatar,
            #     island_map=island_map
            #     levels_coord=levels_coord
            # )
            # db.session.add(new_island)
            # db.session.commit()
            return 'done'
        except:
            return 'failed'
    abort(404, 'Resource not found')

# Islands page
@app.route('/islands')
@login_required
def islands():
    user = current_user
    if user.is_teacher:
        return redirect(url_for('teacher'))
    
    
    group = Groups.query.get(user.group_id)
    group_position = json.loads(group.position)
    math_island = group_position["1"][0]
    scirence_island = group_position["2"][0]

    max_level_math = len(Islands.query.filter_by(lesson=1).all())
    max_level_sci = len(Islands.query.filter_by(lesson=2).all())
    
    islands_math = Islands.query.filter_by(grade=user.grade).filter_by(lesson=1).order_by(Islands.iuid).all()
    islands_science = Islands.query.filter_by(grade=user.grade).filter_by(lesson=2).order_by(Islands.iuid).all()

    math_info = []
    i = 1
    for island in islands_math:
        is_active = False
        is_finished = False

        
        if i == math_island:
            is_active = True
        if i < math_island:
            is_finished = True
        if (math_island == max_level_math) and (group_position["1"][2]):
            is_finished = True
        info = {
            'id': island.iuid,
            'name': island.name,
            'is_active': is_active,
            'is_finished': is_finished,
            'avatar': island.island_avatar
        }
        i+=1
        math_info.append(info)
    
    sc_info = []
    i = 1
    for island in islands_science:
        is_active = False
        is_finished = False

        
        if i == scirence_island:
            is_active = True
        if i < scirence_island:
            is_finished = True
        if (scirence_island == max_level_sci) and (group_position["2"][2]):
            is_finished = True
        info = {
            'id': island.iuid,
            'name': island.name,
            'is_active': is_active,
            'is_finished': is_finished,
            'avatar': island.island_avatar
        }
        i+=1
        sc_info.append(info)

    return render_template(
        'islands.html', 
        user=user, 
        islands_math=math_info,
        islands_sc=sc_info
    )

# Island page
@app.route('/island/<int:island_id>')
@login_required
def island(island_id):
    user = current_user
    if user.is_teacher:
        return redirect(url_for('teacher'))
    
    island = Islands.query.get(int(island_id))
    group = Groups.query.get(int(user.group_id))
    
    position = json.loads(group.position)
    level = position[str(island.lesson)][1]
    current_island = position[str(island.lesson)][0]
    waiting = position[str(island.lesson)][2]

    level_price = int(island.treasure)
    level_price = int((level_price / 2) / (7 - level))

    name = island.name
    map = island.island_map 
    this_map = map[:-4] + str(level) + '.png'

    bio = json.loads(island.bio)
    bio_text = bio[str(level)][1]
    bio_img = bio[str(level)][0] + '.jpg'

    problems = json.loads(island.problems)

    
    group_text_books = TextBooks.query.filter_by(group_id=group.guid).filter_by(island_id=island.iuid).all()
    island_text_books = json.loads(island.text_book)

    max_level = len(Islands.query.filter_by(lesson=island.lesson).all())

    remain_help = 2 - group.help_flag

    dead_time = island.deadline
    jalali_date = jdatetime.datetime.fromgregorian(datetime=dead_time).strftime('%Y/%m/%d')

    group_help = Helps.query.filter_by(requester_id=group.guid).filter_by(island_id=island.iuid).all()
    help_levels = []
    help_id = []
    helper_name = ''
    help_date = ''
    help_rec = False
    for help in group_help:
        if help.is_open:
            help_levels.append(help.level)
            help_id.append(help.huid)
        if (not help.is_open) and (not help.commited):
            helper_name = Groups.query.get(int(help.responser_id)).name
            help_date = jdatetime.datetime.fromgregorian(datetime=help.response_date).strftime('%Y/%m/%d')
            help_rec = True
            help.commited = True
            db.session.commit()

    
    all_helps = Helps.query.filter_by(island_id=island.iuid).all()
    help_needed_groups = []
    for help in all_helps:
        if help.is_open:
            help_needed_groups.append(Groups.query.get(int(help.requester_id)))

    help_needed_groups_name = []
    for team in help_needed_groups:
        if team.guid != group.guid:
            help_needed_groups_name.append([team.guid, team.name])
    
    teacher_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    open_chest = False
    all_groups = Groups.query.filter_by(school=group.school).all()
    num_of_groups = len(all_groups)

    waiting_teams = 0
    for a_group in all_groups:
        g_pos = json.loads(a_group.position)[str(island.lesson)]
        if (g_pos[0] == current_island and (g_pos[2])) or ((g_pos[0] > island_id)):
            waiting_teams += 1

    done_all_islands = False
    if(waiting_teams == num_of_groups):
        next_level = 1
        current_island += 1
        open_chest = True
        if current_island > max_level:
            done_all_islands = True
            open_chest = False
            current_island = max_level
            position[str(island.lesson)] =[current_island, 6, 1]
        else:
            position[str(island.lesson)] =[current_island, next_level, 0]
        new_postion = json.dumps(position)
        group.position = new_postion
        group.money += island.treasure // num_of_groups

        group.help_flag = 0
        group.is_waiting = False
        try:
            db.session.commit()
            print('done')
        except:
            print('failed')
    
    groups_info = []
    for team in all_groups:
        info = []
        if team.school == group.school:
            members = json.loads(team.memebers)
            members_name = []
            for member in members:
                m = Users.query.filter_by(user_name=members[member]).first()
                member_name = m.fname + ' ' + m.lname 
                members_name.append(member_name)
            
            info = [team.avatar, team.name, members_name]
        groups_info.append(info)
            
    print('-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')


    return render_template(
        'island.html',
        island_id=island_id,
        level=level,
        level_price=level_price,
        user=user,
        group_id = group.guid,
        money=group.money,
        name=name,
        map=this_map,
        bio_img=bio_img,
        bio_text=bio_text,
        problems=problems,
        remain_help=remain_help,
        dead_time=jalali_date,
        group_text_books=group_text_books,
        island_text_books=island_text_books,
        help_id=help_id,
        help_levels=help_levels,
        help_needed=help_needed_groups_name,
        helper_name=helper_name,
        help_date=help_date,
        teacher_code=teacher_code,
        waiting=waiting,
        open_chest=open_chest,
        treasure=island.treasure,
        groups_info=groups_info,
        done_all_islands=done_all_islands
    )

# Buy text book API
@app.route('/buy-textbook', methods=["POST"])
def buy_textbook():
    data = request.get_json()
    island_id = data['island_id']
    island = Islands.query.get(int(island_id))
    text_books = json.loads(island.text_book)
    bought_items = data['books']
    spent_money = 0
    group = Groups.query.get(int(current_user.group_id))
    group_text_books = json.loads(group.text_books)
    print(group_text_books[str(island_id)])

    for i in range(len(bought_items)):
        if bought_items[i]:
            print(f"buy {i+1}th text book")
            text_book_info = text_books.get(str(i+1), ['', 0])
            if not group_text_books[str(island_id)][i]:
                spent_money += text_book_info[1]
    
    remain_money = group.money - spent_money
    if remain_money <= 0:
        group.money = 0
        db.session.commit()
        return jsonify({"status": 'low'})


    group_bougt_item = {island_id: bought_items}
    group_text_books.update(group_bougt_item)

    group.text_books = json.dumps(group_text_books)
    group.money = remain_money
    db.session.commit()
    
    return jsonify({"status": 'done'})

# Request help API
@app.route('/req-help', methods=["POST"])
def help_request():
    data = request.get_json()
    new_help = Helps(
        island_id=int(data['island_id']),
        level=int(data['level']),
        requester_id=int(data['group_id'])
    )
    db.session.add(new_help)
    db.session.commit()
    group = Groups.query.get(int(data['group_id']))
    group.help_flag += 1
    db.session.commit()

    return jsonify({"status": 'done'})

# Remove help API
@app.route('/remove-help', methods=["POST"])
def help_remove():
    data = request.get_json()
    help = Helps.query.get_or_404(int(data['help_id']))
    group = Groups.query.get(int(help.requester_id))
    db.session.delete(help)
    db.session.commit()
    group.help_flag -= 1
    db.session.commit()
    
    return jsonify({"status": 'done'})

# Make help API
@app.route('/make-help', methods=["POST"])
def make_help():
    data = request.get_json()
    helps = Helps.query.filter_by(requester_id=int(data['team_id'])).all()
    helper = Groups.query.get(int(current_user.group_id))
    for help in helps:
        if help.is_open:
            help.responser_id = helper.guid
            help.response_date = datetime.utcnow()
            help.is_open = False
    db.session.commit()

    helper.total_helping += 1
    helper.money += 23
    db.session.commit()
    
    return jsonify({"status": 'done'})

# Teacher help API
@app.route('/teacher-help', methods=["POST"])
def teacher_help():
    data = request.get_json()
    group = Groups.query.get(int(current_user.group_id))
    if group.money < 50 :
        return jsonify({"status": 'low'})
    
    group.money -= 50
    db.session.commit()
    return jsonify({"status": 'done'})

# Submit answer API
@app.route('/submit-answer', methods=["POST"])
def submit_answer():
    data = request.get_json()
    island_id = int(data['island_id'])
    level = data['level']
    answer = data['response']
    if answer.replace(".", "").isnumeric():
        if answer.count('.') > 0:
            answer = float(answer)
        else:
            answer = int(answer)
    
    island = Islands.query.get(island_id)
    problems = json.loads(island.problems)
    problem = problems[level]
    expected_answer = problem[-1]
    if expected_answer.replace(".", "").isnumeric():
        if expected_answer.count('.') > 0:
            expected_answer = float(expected_answer)
        else:
            expected_answer = int(expected_answer)

    group = Groups.query.get(int(current_user.group_id))
    grop_position = json.loads(group.position)
    position = grop_position[str(island.lesson)]
    current_island = position[0]
    level = position[1]
    waiting = position[2]

    if answer == expected_answer:
        level += 1
        if(level > 6):
            level = 6
            waiting = 1

        grop_position[str(island.lesson)] =[current_island, level, waiting]
        new_postion = json.dumps(grop_position)
        group.position = new_postion


        level_price = int(island.treasure)
        level_price = int((level_price / 2) / (7 - int(level - 1)))
        last_level_money = 300 + (int((level_price / 2) / (7 - int(level - 1))))
        if (level-1) == 1:
            last_level_money = 300

        if group.money >= last_level_money:
            group.clear_pass += 1
            performance = 1
        else:
            group.just_pass += 1
            performance = 0

        group.money += level_price

        group_activities = json.loads(group.activity)
        this_activity = [island_id, int(level), performance]
        update_activity = False
        for act in group_activities:
                if (act[0] == island_id) and ((act[1] == int(level))):
                    act[2] = performance
                    update_activity = True
        if not update_activity:
            group_activities.append(this_activity)

        group.activity= json.dumps(group_activities)

        db.session.commit()
        if group.level == 6:
            return jsonify({"status": 'complete'})
        return jsonify({"status": 'pass'})
    return jsonify({"status": 'failed'})


# Submit answer API
@app.route('/team-name', methods=["POST"])
def team_name():
    data = request.get_json()
    group = Groups.query.get(int(current_user.group_id))
    group.name = data['name']
    group.avatar = data['avatar']
    db.session.commit()

    return jsonify({"status": 'ok'})

# Profile page
@app.route('/my-profile', methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm()
    user = current_user
    if form.validate_on_submit():
        update_profile = False
        
        user_name = form.user_name.data
        if user_name:
            user.user_name = user_name
            update_profile = True
        fname = form.first_name.data
        lname = form.last_name.data
        if fname and lname:
            user.fname = fname
            user.lname = lname
            update_profile = True
        password = form.password.data
        if password:
            hashed_pass = bcrypt.generate_password_hash(password)
            user.password = hashed_pass
            update_profile = True
        if update_profile:
            try:
                db.session.commit()
                return redirect(url_for('group'))
            except:
                print('fiald')
    print('-----------------------------------------------------')
    return render_template(
        'my-profile.html',
        user=user,
        form=form
    )

# Contact us page
@app.route('/contact-us')
def contact():
    return render_template('contact-us.html', user=current_user)

# About page
@app.route('/about-us')
def about():
    return render_template('about-us.html', user=current_user)

# Start the app
if __name__ == '__main__':
    app.run()