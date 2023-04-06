from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
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
    q1 = StringField('سوال اول(الگو: عنوان سوال-نام عکس-[گزینه ها]-گزینه درست)', validators=[InputRequired(message="لطفا سوال اول را وارد کنید")], render_kw={"placeholder": "مثال: چگونه تقسیم کنیم؟-q1.png-گزینه ها(مثلا [52,51,49,53])-شماره گزینه درست(مثلا 2)"})
    q2 = StringField('سوال دوم(الگو: عنوان سوال-نام عکس-[گزینه ها]-گزینه درست)', validators=[InputRequired(message="لطفا سوال دوم را وارد کنید")], render_kw={"placeholder": "مثال: چگونه تقسیم کنیم؟-q1.png-گزینه ها(مثلا [52,51,49,53])-شماره گزینه درست(مثلا 2)"})
    q3 = StringField('سوال سوم(الگو: عنوان سوال-نام عکس-[گزینه ها]-گزینه درست)', validators=[InputRequired(message="لطفا سوال سوم را وارد کنید")], render_kw={"placeholder": "مثال: چگونه تقسیم کنیم؟-q1.png-گزینه ها(مثلا [52,51,49,53])-شماره گزینه درست(مثلا 2)"})
    q4 = StringField('سوال چهارم(الگو: عنوان سوال-نام عکس-[گزینه ها]-گزینه درست)', validators=[InputRequired(message="لطفا سوال چهارم را وارد کنید")], render_kw={"placeholder": "مثال: چگونه تقسیم کنیم؟-q1.png-گزینه ها(مثلا [52,51,49,53])-شماره گزینه درست(مثلا 2)"})
    q5 = StringField('سوال پنجم(الگو: عنوان سوال-نام عکس-[گزینه ها]-گزینه درست)', validators=[InputRequired(message="لطفا سوال پنجم را وارد کنید")], render_kw={"placeholder": "مثال: چگونه تقسیم کنیم؟-q1.png-گزینه ها(مثلا [52,51,49,53])-شماره گزینه درست(مثلا 2)"})
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