from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, TextAreaField, DateField
from wtforms.validators import InputRequired, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed

cities = ['مشهد', 'تهران', 'اصفهان', 'یزد', 'اهواز', 'تبریز', 'کرج', 'بیرجند', 'بجنورد', 'گرگان', 'زاهدان', 'کرمان']
lessons = ['ریاضی', 'علوم', 'ادبیات', 'عربی', 'زبان', 'هدیه های آسمانی']

class RegisterForm(FlaskForm):
    user_name = StringField('نام کاربری', validators=[InputRequired(message="نام کاربری نمی تواند خالی باشد")], render_kw={"placeholder": "نام کاربری برای ورود به سایت"})
    first_name = StringField('نام', validators=[InputRequired(message="نام خود را وارد کنید")], render_kw={"placeholder": "نام"})
    last_name = StringField('نام خانوادگی', validators=[InputRequired(message="نام خانوادگی خود را وارد کنید")], render_kw={"placeholder": "نام خانوادگی"})
    personal_id = StringField('کد ملی', validators=[InputRequired(message="کد ملی نمی تواند خالی باشد"), Length(min=10, max=10, message="کد ملی نامعتبر")], render_kw={"placeholder": "کد ملی"})
    phone = StringField('تلفن همراه', validators=[InputRequired(message="تلفن همراه نمی تواند خالی باشد"), Length(min=11, max=11, message="تلفن همراه نامعتبر")], render_kw={"placeholder": "تلفن همراه"})
    password = PasswordField('رمز عبور', validators=[InputRequired(message="یک رمز عبور انتخاب کنید"), Length(min=8, max=20, message="رمز باید حداقل 8 کاراکتر داشته اشد")], render_kw={"placeholder": "رمزعبور"})
    repeat_password = PasswordField('تکرار رمز عبور', validators=[InputRequired(message="رمز عبور خود را تکرار کنید"), EqualTo('password', message="تکرار رمز و رمز با یکدیگر یکسان نیستند!")], render_kw={"placeholder": "تکرار رمزعبور"})
    grade = IntegerField('پایه تحصیلی', validators=[InputRequired(message="پایه تحصیلی خود را وارد کنید")], render_kw={"placeholder": "پایه تحصیلی هدف"})
    section = SelectField('مقطع تحصیلی', choices=[('1', 'متوسطه اول'), ('2', 'متوسطه دوم'), ('0', 'ابتدایی')])
    school_name = StringField('نام مرکز آموزشی', validators=[InputRequired(message="نام مرکز نمی تواند خالی باشد")], render_kw={"placeholder": "نام مرکز آموزشی"})
    city = SelectField('شهر', choices=[(c, c) for c in cities])
    gender = SelectField('جنسیت', choices=[('1', 'دخترانه'), ('2', 'پسرانه')])
    submit = SubmitField('ثبت نام')


class LoginForm(FlaskForm):
    user_name = StringField('نام کاربری', validators=[InputRequired(message="لطفا نام کاربری را وارد کنید")], render_kw={"placeholder": "نام کاربری"})
    password = PasswordField('رمزعبور', validators=[InputRequired(message="لطفا رمز عبور را وارد کنید"), Length(min=8, max=20, message="رمز عبور نمی تواند کمتر از 8 کاراکتر باشد!")], render_kw={"placeholder": "رمزعبور"})
    remember_me = BooleanField('مرا بخاطر بسپار')
    submit = SubmitField('ورود')

class StudentsSetupForm(FlaskForm):
    class_name = StringField('نام کلاس', validators=[InputRequired(message="لطفا نام کلاس را وارد کنید")], render_kw={"placeholder": "نام کلاس"})
    nums = IntegerField('تعداد انش آموزان', validators=[InputRequired(message="لطفا تعداد انش آموزان را وارد کنید")], render_kw={"placeholder": "تعداد دانش آموزان"})
    def_pass = StringField('رمز پیشفرض', validators=[InputRequired(message="لطفا رمز پیش فرض را وارد کنید")], render_kw={"placeholder": "رمز پیشفرض برای همه"})
    submit = SubmitField('ساخت فرم ثبت نام')


class CreateIslandForm(FlaskForm):
    name = StringField('نام', validators=[InputRequired(message="نام جزیره را وارد کنید")], render_kw={"placeholder": "نام جزیره"})
    grade = IntegerField('پایه تحصیلی', validators=[InputRequired(message="پایه تحصیلی را وارد کنید")], render_kw={"placeholder": "پایه تحصیلی هدف"})
    lesson = SelectField('درس', choices=[(lessons.index(l) + 1, l) for l in lessons])
    start_date = DateField('تاریخ شروع', validators=[InputRequired(message="تاریخ شروع را وارد کنید")], render_kw={"placeholder": "تاریخ شروع"})
    end_date = DateField('تاریخ پایان', validators=[InputRequired(message="تاریخ پایان را وارد کنید")], render_kw={"placeholder": "تاریخ پایان"})
    avatar = StringField('تصویر جزیره', validators=[InputRequired(message="تصویر جزیره را وارد کنید")], render_kw={"placeholder": "آدرس تصویر جزیره"})
    map = StringField('تصویر نقشه جزیره', validators=[InputRequired(message="نقشه جزیره را وارد کنید")], render_kw={"placeholder": "نام تصویر نقشه جزیره"})
    p1 = StringField('چالش اول', validators=[InputRequired(message="چالش اول را وارد کنید")], render_kw={"placeholder": "چالش اول(بصورت آدرس تصویر مثلا img/...)"})
    a1 = StringField('پاسخ چالش اول', validators=[InputRequired(message="پاسخ چالش اول را وارد کنید")], render_kw={"placeholder": "پاسخ صحیح چالش اول"})
    p2 = StringField('چالش دوم', validators=[InputRequired(message="چالش دوم را وارد کنید")], render_kw={"placeholder": "چالش دوم(بصورت آدرس تصویر مثلا img/...)"})
    a2 = StringField('پاسخ چالش دوم', validators=[InputRequired(message="پاسخ چالش دوم را وارد کنید")], render_kw={"placeholder": "پاسخ صحیح چالش دوم"})
    p3 = StringField('چالش سوم', validators=[InputRequired(message="چالش سوم را وارد کنید")], render_kw={"placeholder": "چالش سوم(بصورت آدرس تصویر مثلا img/...)"})
    a3 = StringField('پاسخ چالش سوم', validators=[InputRequired(message="پاسخ چالش سوم را وارد کنید")], render_kw={"placeholder": "پاسخ صحیح چالش سوم"})
    p4 = StringField('چالش چهارم', validators=[InputRequired(message="چالش چهارم را وارد کنید")], render_kw={"placeholder": "چالش چهارم(بصورت آدرس تصویر مثلا img/...)"})
    a4 = StringField('پاسخ چالش چهارم', validators=[InputRequired(message="پاسخ چالش چهارم را وارد کنید")], render_kw={"placeholder": "پاسخ صحیح چالش چهارم"})
    p5 = StringField('چالش پنجم', validators=[InputRequired(message="چالش پنجم را وارد کنید")], render_kw={"placeholder": "چالش پنجم(بصورت آدرس تصویر مثلا img/...)"})
    a5 = StringField('پاسخ چالش پنجم', validators=[InputRequired(message="پاسخ چالش پنجم را وارد کنید")], render_kw={"placeholder": "پاسخ صحیح چالش پنجم"})
    p6 = StringField('چالش ششم', validators=[InputRequired(message="چالش ششم را وارد کنید")], render_kw={"placeholder": "چالش ششم(بصورت آدرس تصویر مثلا img/...)"})
    a6 = StringField('پاسخ چالش ششم', validators=[InputRequired(message="پاسخ چالش ششم را وارد کنید")], render_kw={"placeholder": "پاسخ صحیح چالش ششم"})
    t1 = StringField('درسنامه اول', validators=[InputRequired(message="درسنامه اول را وارد کنید")], render_kw={"placeholder": "اسم عکس درسنامه اول"})
    t2 = StringField('درسنامه دوم', validators=[InputRequired(message="درسنامه دوم را وارد کنید")], render_kw={"placeholder": "اسم عکس درسنامه دوم"})
    t3 = StringField('درسنامه سوم', validators=[InputRequired(message="درسنامه سوم را وارد کنید")], render_kw={"placeholder": "اسم عکس درسنامه سوم"})
    treasure = IntegerField('جایزه نهایی', validators=[InputRequired(message="جایزه نهایی را وارد کنید")], render_kw={"placeholder": "جایزه نهایی(تعداد سکه)"})
    scientist = StringField('اسم عکس دانشمند', validators=[InputRequired(message="اسم عکس دانشمند را وارد کنید")], render_kw={"placeholder": "اسم عکس دانشمند جزیره(مثلا ax1)"})
    b1 = TextAreaField('بیوگرافی 1', validators=[InputRequired(message="بیوگرافی را وارد کنید")], render_kw={"placeholder": "بیوگرافی دانشمند برای مرحله 1"})
    b2 = TextAreaField('بیوگرافی 2', validators=[InputRequired(message="بیوگرافی را وارد کنید")], render_kw={"placeholder": "بیوگرافی دانشمند برای مرحله 2"})
    b3 = TextAreaField('بیوگرافی 3', validators=[InputRequired(message="بیوگرافی را وارد کنید")], render_kw={"placeholder": "بیوگرافی دانشمند برای مرحله 3"})
    b4 = TextAreaField('بیوگرافی 4', validators=[InputRequired(message="بیوگرافی را وارد کنید")], render_kw={"placeholder": "بیوگرافی دانشمند برای مرحله 4"})
    b5 = TextAreaField('بیوگرافی 5', validators=[InputRequired(message="بیوگرافی را وارد کنید")], render_kw={"placeholder": "بیوگرافی دانشمند برای مرحله 5"})
    b6 = TextAreaField('بیوگرافی 6', validators=[InputRequired(message="بیوگرافی را وارد کنید")], render_kw={"placeholder": "بیوگرافی دانشمند برای مرحله 6"})
    
    submit = SubmitField('ساخت جزیره')

class ProfileForm(FlaskForm):
    profile_picture = FileField('تصویر کاریری', validators=[FileAllowed(['jpg', 'png'], message="فرمت فایل غیر مجاز است.")], render_kw={"placeholder": "آواتار"})
    user_name = StringField('نام کاربری', render_kw={"placeholder": "نام کاربری برای ورود به سایت"})
    first_name = StringField('نام', render_kw={"placeholder": "نام"})
    last_name = StringField('نام خانوادگی', render_kw={"placeholder": "نام خانوادگی"})
    password = PasswordField('رمز عبور', render_kw={"placeholder": "رمزعبور جدید"})
    repeat_password = PasswordField('تکرار رمز عبور', validators=[EqualTo('password', message="تکرار رمز و رمز با یکدیگر یکسان نیستند!")], render_kw={"placeholder": "تکرار رمزعبور"})
    submit = SubmitField('دخیره تغییرات')