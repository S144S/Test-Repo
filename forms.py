from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    first_name = StringField('نام', validators=[InputRequired(message="نمی تواند خالی باشد")], render_kw={"placeholder": "نام"})
    last_name = StringField('نام خانوادگی', validators=[InputRequired(message="نمی تواند خالی باشد")], render_kw={"placeholder": "نام خانوادگی"})
    password = PasswordField('رمز', validators=[InputRequired(message="نمی تواند خالی باشد"), Length(min=8, max=20, message="کوتاه است")], render_kw={"placeholder": "رمزعبور"})
    repeat_password = PasswordField('تکرار رمز', validators=[InputRequired(message="نمی تواند خالی باشد"), EqualTo('password', message="با رمز یکسان نیست")], render_kw={"placeholder": "تکرار رمز"})
    phone = StringField('شماره تلفن', validators=[InputRequired(message="نمی تواند خالی باشد")], render_kw={"placeholder": "تلفن همراه"})
    submit = SubmitField('ثبت نام')


class LoginForm(FlaskForm):
    phone = StringField('شماره تلفن', validators=[InputRequired(message="لطفا شماره تلفن خود را وارد کنید")], render_kw={"placeholder": "شماره تلفن همراه"})
    password = PasswordField('رمزعبور', validators=[InputRequired(message="لطفا رمز عبور را وارد کنید"), Length(min=8, max=20, message="رمز عبور نمی تواند کمتر از 8 کاراکتر باشد!")], render_kw={"placeholder": "رمزعبور"})
    remember_me = BooleanField('مرا بخاطر بسپار')
    submit = SubmitField('ورود')

class AddCorpsForm(FlaskForm):
    name = StringField('نام محصول', validators=[InputRequired(message="نام محصول را وراد کنید")], render_kw={"placeholder": "نام محصول"})
    max_temp = IntegerField('حداکثر دمای قابل تحمل', validators=[InputRequired(message='نمی تواند خالی باشد')], render_kw={"placeholder": "حداکثر دمای قابل تحمل محصول"})
    min_temp = IntegerField('حداقل دمای قابل تحمل', render_kw={"placeholder": "حداقل دمای قابل تحمل محصول"})
    max_hum = IntegerField('حداکثر رطوبت قابل تحمل', validators=[InputRequired(message='نمی تواند خالی باشد')], render_kw={"placeholder": "حداکثر رطوبت قابل تحمل محصول"})
    min_hum = IntegerField('حداقل رطوبت قابل تحمل', render_kw={"placeholder": "حداقل رطوبت قابل تحمل محصول"})
    submit = SubmitField('ذخیره')

class AddCityForm(FlaskForm):
    name = StringField('نام شهر', validators=[InputRequired(message="نام شهر را وراد کنید")], render_kw={"placeholder": "نام شهر"})
    altitude = IntegerField('ارتفاع از سطح دریا', validators=[InputRequired(message='نمی تواند خالی باشد')], render_kw={"placeholder": "ارتفاع از سطح دریا(متر)"})
    submit = SubmitField('ذخیره')

class UpdateProfileForm(FlaskForm):
    password = PasswordField('رمز', validators=[InputRequired(message="نمی تواند خالی باشد"), Length(min=8, max=20, message="کوتاه است")], render_kw={"placeholder": "رمزعبور"})
    repeat_password = PasswordField('تکرار رمز', validators=[InputRequired(message="نمی تواند خالی باشد"), EqualTo('password', message="با رمز یکسان نیست")], render_kw={"placeholder": "تکرار رمز"})
    phone = StringField('شماره تلفن', validators=[InputRequired(message="نمی تواند خالی باشد")], render_kw={"placeholder": "تلفن همراه"})
    submit = SubmitField('بروزرسانی')