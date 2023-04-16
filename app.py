from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_migrate import Migrate
from models import db, Users, Records, Corps, Cities
from forms import *
import secrets
from flask_bcrypt import Bcrypt
import pytz
import datetime
import jdatetime
from sqlalchemy import func
import math
from weather import get_weather

# Initializing the app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.debug = True
app.config['SECRET_KEY'] = 'FarzanSchool'

# Initializing upload image
# UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Setting time zone
utc_tz = pytz.timezone('UTC')
local_tz = pytz.timezone('Asia/Tehran')

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

#####################################################################
@app.route('/register', methods=('GET', 'POST'))
@login_required
def register():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        is_admin = False
        password = form.password.data
        hashed_pass = bcrypt.generate_password_hash(password)
        fname = form.first_name.data
        lname = form.last_name.data
        phone = form.phone.data
        if('72412' in phone):
            is_admin = True
        gen_token =  secrets.token_urlsafe(16)
        
        
        new_user = Users(phone=phone, password = hashed_pass, fname=fname, lname=lname,
                            is_admin=is_admin, ak_token = gen_token)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Login page
@app.route('/login', methods=('GET', 'POST'))
def login():
    # Already logged user does not need to login page
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        phone = form.phone.data
        password = form.password.data
        user = Users.query.filter_by(phone=phone).first()
        if user:
            print('success')
            check_pass = bcrypt.check_password_hash(user.password, password)
            if check_pass:
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
        print(user)
    return render_template('login.html', form=form)

# Logout page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Home page
@app.route('/')
@app.route('/home')
@login_required
def home():
    record = Records.query.filter_by(user_id=current_user.uid).order_by(Records.creation_date.desc()).first()
    last_update = jdatetime.datetime.fromgregorian(datetime=record.creation_date)
    last_update_date = last_update.strftime('%Y/%m/%d')
    local_time = utc_tz.localize(record.creation_date).astimezone(local_tz)
    last_update_time = local_time.strftime("%H:%M:%S")

    return render_template(
        'index.html', 
        user=current_user, 
        record=record, 
        update_date=last_update_date, 
        update_time=last_update_time
        )

# Data API
@app.route('/api/data', methods=["POST"])
def get_data():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(' ')[1] if auth_header else None
    if token:
        user = Users.query.filter_by(ak_token=token).first()
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'No data provided'}), 400
        if not isinstance(data, dict):
            return jsonify({'error': 'Data must be a dictionary'}), 400
        if ('temperature' not in data) or not isinstance(data['temperature'], float):
            return jsonify({'error': 'temperature is missing from data'}), 400
        if ('pressure' not in data) or not isinstance(data['pressure'], int):
            return jsonify({'error': 'pressure is missing from data'}), 400
        if ('humidity' not in data) or not isinstance(data['humidity'], int):
            return jsonify({'error': 'humidity is missing from data'}), 400
        if ('light' not in data) or not isinstance(data['light'], int):
            return jsonify({'error': 'light is missing from data'}), 400
        if ('rain' not in data) or not isinstance(data['rain'], int):
            return jsonify({'error': 'rain is missing from data'}), 400
        if ('soil' not in data) or not isinstance(data['soil'], int):
            return jsonify({'error': 'soil is missing from data'}), 400
        if ('alarm' not in data) or not isinstance(data['alarm'], int):
            return jsonify({'error': 'alarm is missing from data'}), 400
        if ('charge' not in data) or not isinstance(data['charge'], int):
            return jsonify({'error': 'charge is missing from data'}), 400
        
        new_record = Records(
            user_id=user.uid, 
            temperature=data['temperature'],
            pressure=data['pressure'],
            humidity=data['humidity'],
            light=data['light'],
            rain=data['rain'],
            soil=data['soil'],
            alarm=data['alarm'],
            charge=data['charge']
            )
        db.session.add(new_record)
        db.session.commit()

    return jsonify({'status': 'submitted'})

# Update data API
@app.route('/api/update')
def update_data():
    record = Records.query.filter_by(user_id=current_user.uid).order_by(Records.creation_date.desc()).first()
    last_update = jdatetime.datetime.fromgregorian(datetime=record.creation_date)
    last_update_date = last_update.strftime('%Y/%m/%d')
    local_time = utc_tz.localize(record.creation_date).astimezone(local_tz)
    last_update_time = local_time.strftime("%H:%M:%S")
    return jsonify({
        'temperature': record.temperature,
        'pressure': record.pressure,
        'humidity': record.humidity,
        'light': record.light,
        'rain': record.rain,
        'soil': record.soil,
        'alarm': record.alarm,
        'charge': record.charge,
        'temperature': record.temperature,
        'last_update_date': last_update_date,
        'last_update_time': last_update_time
        })

# Details page
@app.route('/detail')
def detail():
    return render_template('details.html', user=current_user)

# Update charts data API
@app.route('/api/chart/update')
def update_charts():
    today = datetime.date.today()
    start_of_day = datetime.datetime.combine(today, datetime.datetime.min.time())
    end_of_day = datetime.datetime.combine(today, datetime.datetime.max.time())

    temp_values = db.session.query(func.strftime('%H', Records.creation_date).label('hour'),
                               func.avg(Records.temperature).label('average_value')).group_by('hour').filter(Records.creation_date >= start_of_day, Records.creation_date <= end_of_day).all()
    temp_hour_dict = {str(h): int(v) for h, v in temp_values}
    new_temp_data = [temp_hour_dict.get(str(h).zfill(2), None) for h in range(0, 24)]

    hum_values = db.session.query(func.strftime('%H', Records.creation_date).label('hour'),
                               func.avg(Records.humidity).label('average_value')).group_by('hour').filter(Records.creation_date >= start_of_day, Records.creation_date <= end_of_day).all()
    hum_hour_dict = {str(h): int(v) for h, v in hum_values}
    new_hum_data = [hum_hour_dict.get(str(h).zfill(2), None) for h in range(0, 24)]

    press_values = db.session.query(func.strftime('%H', Records.creation_date).label('hour'),
                               func.avg(Records.pressure).label('average_value')).group_by('hour').filter(Records.creation_date >= start_of_day, Records.creation_date <= end_of_day).all()
    press_hour_dict = {str(h): int(v) for h, v in press_values}
    new_press_data = [press_hour_dict.get(str(h).zfill(2), None) for h in range(0, 24)]

    lux_values = db.session.query(func.strftime('%H', Records.creation_date).label('hour'),
                                  func.avg(Records.light).label('average_value')).group_by('hour').filter(Records.creation_date >= start_of_day, Records.creation_date <= end_of_day).all()
    lux_hour_dict = {str(h): int(v) for h, v in lux_values}
    new_lux_data = [lux_hour_dict.get(str(h).zfill(2), None) for h in range(0, 24)]

    return jsonify({
        'temp': new_temp_data,
        'hum': new_hum_data,
        'press': new_press_data,
        'lux': new_lux_data
    })

# Setting page
@app.route('/setting')
@login_required
def setting():
    corps = Corps.query.all()
    corps_dict = {}
    for corp in corps:
        corps_dict[corp.cid] = corp.name

    cities = Cities.query.all()
    cities_dict = {}
    for city in cities:
        cities_dict[city.cid] = city.name

    return render_template('setting.html', user=current_user, corps=corps_dict, cities=cities_dict)

# Update charts data API
@app.route('/api/add/corps')
def add_corps():
    user_id = current_user.uid
    corps_name = "انار"
    max_temp = 40
    min_temp = 0
    max_hum = 0
    min_hum = 0

    # new_corps = Corps(name=corps_name, max_temp=max_temp, min_temp=min_temp)
    # db.session.add(new_corps)
    # db.session.commit()
    return 'done'

# Add new corps
@app.route('/add-corps', methods=["GET", "POST"])
@login_required
def add_new_corps():
    form = AddCorpsForm()
    if form.validate_on_submit():
        name = form.name.data
        max_temp = form.max_temp.data
        min_temp = form.min_temp.data
        max_hum = form.max_hum.data
        min_hum = form.min_hum.data
        new_corps = Corps(name=name, max_temp=max_temp, min_temp=min_temp, max_hum=max_hum, min_hum=min_hum)
        try:
            db.session.add(new_corps)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            return render_template('add-corps.html', user=current_user, form=form)

    return render_template('add-corps.html', user=current_user, form=form)

# Add new city
@app.route('/add-city', methods=["GET", "POST"])
@login_required
def add_city():
    user = current_user
    form = AddCityForm()
    if form.validate_on_submit():
        name = form.name.data
        altitude = form.altitude.data

        new_city = Cities(name=name, altitude=altitude)
        try:
            db.session.add(new_city)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            return render_template('add-city.html', user=user, form=form)
    return render_template('add-city.html', user=user, form=form)

# Get setting API
@app.route('/api/setting', methods=["POST"])
def get_stting():
    data = request.get_json()
    print(data)

    current_user.active_alarm = data['alarm']
    current_user.corps_id = int(data['corp'])
    city = Cities.query.get(int(data['city']))
    current_user.city = city.name
    db.session.commit()

    return jsonify({'status': True})

# Check for alarm API
@app.route('/api/is-alarm', methods=["POST"])
def is_alarm():
    data = request.get_json()
    phone = data['phone']
    user = Users.query.filter_by(phone=phone).first()
    record = Records.query.filter_by(user_id=user.uid).order_by(Records.creation_date.desc()).first()
    user_city = user.city
    city = Cities.query.filter_by(name=user_city).first()
    user_corp = int(user.corps_id)
    corp = Corps.query.get(user_corp)

    city_altitude = city.altitude
    max_temp = corp.max_temp
    min_temp = corp.min_temp
    w = get_weather(user.city)
    alarm = 0
    

    today_min = int(w['d0_min_temp'])
    d1_min = int(w['d1_min_temp'])
    d2_min = int(w['d2_min_temp'])
    today_max = int(w['d0_max_temp'])
    temperature = record.temperature
    min_temp_allowed = corp.min_temp
    wind = int(w['wind'][:w['wind'].index(' ')])
    precipitation = int(w['precipitation'][:w['precipitation'].index('%')])
    pressure = record.pressure
    T0 = 288.15
    L = 0.0065
    P0 = 101325
    R = 287.05
    g = 9.80665
    altitude = int((T0 / L) * (1 - (pressure / P0) ** (R * L / g)))
    temp_num_d1 = d1_min - min_temp_allowed
    temp_num_d2 = d2_min - min_temp_allowed
    alt_num = altitude - city_altitude

    alt_chill = alt_num * 0.0065
    wind_chill_today = 13.12 + (0.6215 * temperature) - 11.37 * wind**0.16 + 0.3965 * temperature * wind**0.16
    real_feel_today = wind_chill_today + alt_chill 
    print(real_feel_today, wind_chill_today, alt_chill)

    if real_feel_today < min_temp_allowed:
        alarm = 1
    if temp_num_d1 < min_temp_allowed or temp_num_d2 < min_temp_allowed:
        alarm = 2



    return jsonify({'state': alarm})

# Weather report page
@app.route('/weather')
@login_required
def weather():
    user = current_user
    w = get_weather(user.city)
    record = Records.query.filter_by(user_id=user.uid).order_by(Records.creation_date.desc()).first()

    return render_template('weather.html', user=user, weather=w, record=record)

# User profile page
@app.route('/profile')
@login_required
def profile():
    user = current_user
    form = UpdateProfileForm()
    if form.validate_on_submit():
        phone = form.phone.data
        password = form.password.data
        hashed_pass = bcrypt.generate_password_hash(password)
        user.phone = phone
        user.password = password
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('profile.html', user=user, form=form)

# User profile page
@app.route('/contact-us')
def contact():
    return render_template('contact.html', user=current_user)

# Start the app
if __name__ == '__main__':
    app.run()