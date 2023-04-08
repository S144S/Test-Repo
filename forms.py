from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    user_name = StringField('نام کاربری', validators=[InputRequired(message="نام کاربری نمی تواند خالی باشد")], render_kw={"placeholder": "نام کاربری"})
    first_name = StringField('نام', validators=[InputRequired(message="نام خود را وارد کنید")], render_kw={"placeholder": "نام"})
    last_name = StringField('نام خانوادگی', validators=[InputRequired(message="نام خانوادگی خود را وارد کنید")], render_kw={"placeholder": "نام خانوادگی"})
    password = PasswordField('رمز عبور', validators=[InputRequired(message="یک رمز عبور انتخاب کنید"), Length(min=8, max=20, message="رمز باید حداقل 8 کاراکتر داشته اشد")], render_kw={"placeholder": "رمزعبور"})
    repeat_password = PasswordField('تکرار رمز عبور', validators=[InputRequired(message="رمز عبور خود را تکرار کنید"), EqualTo('password', message="تکرار رمز و رمز با یکدیگر یکسان نیستند!")], render_kw={"placeholder": "تکرار رمزعبور"})
    grade = IntegerField('پایه تحصیلی', validators=[InputRequired(message="پایه تحصیلی خود را وارد کنید")], render_kw={"placeholder": "پایه تحصیلی"})
    submit = SubmitField('ثبت نام')


class LoginForm(FlaskForm):
    user_name = StringField('نام کاربری', validators=[InputRequired(message="لطفا نام کاربری را وارد کنید")], render_kw={"placeholder": "نام کاربری"})
    password = PasswordField('رمزعبور', validators=[InputRequired(message="لطفا رمز عبور را وارد کنید"), Length(min=8, max=20, message="رمز عبور نمی تواند کمتر از 8 کاراکتر باشد!")], render_kw={"placeholder": "رمزعبور"})
    remember_me = BooleanField('مرا بخاطر بسپار')
    submit = SubmitField('ورود')


class AddCourseForm(FlaskForm):
    grade = IntegerField('پایه تحصیلی', validators=[InputRequired(message="پایه تحصیلی را وارد کنید")], render_kw={"placeholder": "پایه تحصیلی"})
    lesson = IntegerField('درس', validators=[InputRequired(message="درس را وارد کنید")], render_kw={"placeholder": "درس"})
    session = IntegerField('فصل', validators=[InputRequired(message="فصل را وارد کنید")], render_kw={"placeholder": "فصل"})
    script = StringField('نام فایل عکس درسنامه', validators=[InputRequired(message="لطفا نام فایل را وارد کنید")], render_kw={"placeholder": "نام فایل(مثلا test.jpg)"})
    video = StringField('کد فیلم کلی اصلی درس', validators=[InputRequired(message="لطفا کد فیلم را وارد کنید")], render_kw={"placeholder": "کد فیلم(مثلا yQbWO)"})
    deaf = StringField('کد فیلم کلی ناشنوایان درس', validators=[InputRequired(message="لطفا کد فیلم ناشنوایان را وارد کنید")], render_kw={"placeholder": "کد فیلم(مثلا yQbWO)"})
    sec1 = StringField('محتوای بخش اول(الگو: عنوان بخش-کد فیلم-کد فیلم ناشنوا-اسم عکس درسنامه)', validators=[InputRequired(message="لطفا محتوای بخش اول را وارد کنید")], render_kw={"placeholder": "'بخش اول'-'کد فیلم'-'کد فیلم ناشنوا'-'اسم کامل عکس'"})
    sec2 = StringField('محتوای بخش دوم(الگو: عنوان بخش-کد فیلم-کد فیلم ناشنوا-اسم عکس درسنامه)', validators=[InputRequired(message="لطفا محتوای بخش دوم را وارد کنید")], render_kw={"placeholder": "'بخش دوم'-'کد فیلم'-'کد فیلم ناشنوا'-'اسم کامل عکس'"})
    sec3 = StringField('محتوای بخش سوم(الگو: عنوان بخش-کد فیلم-کد فیلم ناشنوا-اسم عکس درسنامه)', validators=[InputRequired(message="لطفا محتوای بخش سوم را وارد کنید")], render_kw={"placeholder": "'بخش سوم'-'کد فیلم'-'کد فیلم ناشنوا'-'اسم کامل عکس'"})
    q1 = StringField('اسم تصویر سوال اول', validators=[InputRequired(message="لطفا سوال اول را وارد کنید")], render_kw={"placeholder": "q1.png"})
    q2 = StringField('اسم تصویر سوال دوم', validators=[InputRequired(message="لطفا سوال دوم را وارد کنید")], render_kw={"placeholder": "q1.png"})
    q3 = StringField('اسم تصویر سوال سوم', validators=[InputRequired(message="لطفا سوال سوم را وارد کنید")], render_kw={"placeholder": "q1.png"})
    q4 = StringField('اسم تصویر سوال چهارم', validators=[InputRequired(message="لطفا سوال چهارم را وارد کنید")], render_kw={"placeholder": "q1.png"})
    q5 = StringField('اسم تصویر سوال پنجم', validators=[InputRequired(message="لطفا سوال پنجم را وارد کنید")], render_kw={"placeholder": "q1.png"})
    o1 = StringField('گزینه های سوال اول)', validators=[InputRequired(message="لطفا گزینه ها را وارد کنید")], render_kw={"placeholder": "گزینه ها(هر گزینه را با خط تیره جدا کنید)"})
    o2 = StringField('گزینه های سوال دوم)', validators=[InputRequired(message="لطفا گزینه ها را وارد کنید")], render_kw={"placeholder": "گزینه ها(هر گزینه را با خط تیره جدا کنید)"})
    o3 = StringField('گزینه های سوال سوم)', validators=[InputRequired(message="لطفا گزینه ها را وارد کنید")], render_kw={"placeholder": "گزینه ها(هر گزینه را با خط تیره جدا کنید)"})
    o4 = StringField('گزینه های سوال چهارم)', validators=[InputRequired(message="لطفا گزینه ها را وارد کنید")], render_kw={"placeholder": "گزینه ها(هر گزینه را با خط تیره جدا کنید)"})
    o5 = StringField('گزینه های سوال پنجم)', validators=[InputRequired(message="لطفا گزینه ها را وارد کنید")], render_kw={"placeholder": "گزینه ها(هر گزینه را با خط تیره جدا کنید)"})
    c1 = StringField('شماره صحیح سوال اول)', validators=[InputRequired(message="لطفا گزینه صحیح را وارد کنید")], render_kw={"placeholder": "مثلا 1"})
    c2 = StringField('شماره صحیح سوال دوم)', validators=[InputRequired(message="لطفا گزینه صحیح را وارد کنید")], render_kw={"placeholder": "مثلا 1"})
    c3 = StringField('شماره صحیح سوال سوم)', validators=[InputRequired(message="لطفا گزینه صحیح را وارد کنید")], render_kw={"placeholder": "مثلا 1"})
    c4 = StringField('شماره صحیح سوال چهارم)', validators=[InputRequired(message="لطفا گزینه صحیح را وارد کنید")], render_kw={"placeholder": "مثلا 1"})
    c5 = StringField('شماره صحیح سوال پنجم)', validators=[InputRequired(message="لطفا گزینه صحیح را وارد کنید")], render_kw={"placeholder": "مثلا 1"})
    submit = SubmitField('ثبت محتوا')

class AddCouponForm(FlaskForm):
    code = StringField('کد جایزه', validators=[InputRequired(message="لطفا کد جایزه را وارد کنید")], render_kw={"placeholder": "کد جایزه"})
    description = StringField('توضیحات جایزه', render_kw={"placeholder": "توضیحات"})
    expire_date = DateField('تاریخ انقضا')
    submit = SubmitField('ثبت جایزه', render_kw={"placeholder": "تاریخ انقضا"})

class UpdateUserForm(FlaskForm):
    user_name = StringField('نام کاربری', validators=[InputRequired(message="نام کاربری نمی تواند خالی باشد")], render_kw={"placeholder": "نام کاربری"})
    first_name = StringField('نام', validators=[InputRequired(message="نام خود را وارد کنید")], render_kw={"placeholder": "نام"})
    last_name = StringField('نام خانوادگی', validators=[InputRequired(message="نام خانوادگی خود را وارد کنید")], render_kw={"placeholder": "نام خانوادگی"})
    password = PasswordField('رمز عبور', validators=[InputRequired(message="یک رمز عبور انتخاب کنید"), Length(min=8, max=20, message="رمز باید حداقل 8 کاراکتر داشته اشد")], render_kw={"placeholder": "رمزعبور"})
    repeat_password = PasswordField('تکرار رمز عبور', validators=[InputRequired(message="رمز عبور خود را تکرار کنید"), EqualTo('password', message="تکرار رمز و رمز با یکدیگر یکسان نیستند!")], render_kw={"placeholder": "تکرار رمزعبور"})
    submit = SubmitField('دخیره تغییرات')

class AskForm(FlaskForm):
    full_name = StringField('نام کامل', validators=[InputRequired(message="نام نمی تواند خالی باشد")])
    shad = StringField('آیدی شاد', validators=[InputRequired(message="آیدی شاد نمی تواند خالی باشد")])
    grade = IntegerField('پایه تحصیلی', validators=[InputRequired(message="پایه تحصیلی را وارد کنید")])
    subject = StringField('عنوان', validators=[InputRequired(message="عنوان نمی تواند خالی باشد")])
    text = TextAreaField('پیام', validators=[InputRequired(message="پیام نمی تواند خالی باشد")])
    submit = SubmitField('ارسال پیام')
