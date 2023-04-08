/*!
	* Toasts
	* 
	* 
*/

if (document.readyState == 'loading') 
{
    document.addEventListener('DOMContentLoaded', main)
} 
else 
{
    main()
}

function main() {
    let formBut = document.querySelector('#create-form');
    formBut.addEventListener('click', createForm);
}

function createForm() {
    let classNameAlarm = document.querySelector('#class-alarm');
    let numberAlarm = document.querySelector('#num-alarm');
    let passAlarm = document.querySelector('#pass-alarm');
    let grageAlarm = document.querySelector('#grage-alarm');
    let className = document.querySelector('#class-name').value;
    let grade = document.querySelector('#stu-grade').value;
    let num = document.querySelector('#stu-nums').value;
    let pass = document.querySelector('#default-pass').value;
    if(!className) {
        numberAlarm.classList.add('d-none');
        passAlarm.classList.add('d-none');
        grageAlarm.classList.add('d-none');
        classNameAlarm.classList.remove('d-none');
        return;
    }
    if(!grade) {
        numberAlarm.classList.add('d-none');
        passAlarm.classList.add('d-none');
        grageAlarm.classList.remove('d-none');
        classNameAlarm.classList.add('d-none');
        return;
    }
    if((!num) || (parseInt(num) < 6)) {
        classNameAlarm.classList.add('d-none');
        passAlarm.classList.add('d-none');
        grageAlarm.classList.add('d-none');
        numberAlarm.classList.remove('d-none');
        return;
    }
    if(!pass) {
        classNameAlarm.classList.add('d-none');
        numberAlarm.classList.add('d-none');
        grageAlarm.classList.add('d-none');
        passAlarm.classList.remove('d-none');
        return;
    }
    classNameAlarm.classList.add('d-none');
    numberAlarm.classList.add('d-none');
    passAlarm.classList.add('d-none');

    let formContainer = document.querySelector('#student-form');
    let group_num = 0
    if(num % 3 == 0) {
        group_num = Math.floor(num/3)
    }
    else {
        group_num = Math.floor(num/3) + 1
    }
    let description = "<p>شما می توانید "
    description += String(group_num)
    description += " گروه بسازید"
    description += ". ابتدا گروه های سه نفره را تکمیل کنید سپس دانش آموزان باقی مانده را در گروه های دو نفره نقسیم کنید."
    description += "</p>"
    formContainer.innerHTML = description;
    for(let i = 0; i < num; i++) {
        formContainer.innerHTML += `                        
        <div class="form-group row student-info">
            <div class="col-sm-3 mb-3 mb-sm-0">
                <input type="text" class="form-control text-white student-fname" placeholder="نام دانش آموز">
            </div>
            <div class="col-sm-3 mb-3">
                <input type="text" class="form-control text-white student-lname" placeholder="نام خانوادگی دانش آموز">
            </div>
            <div class="col-sm-3 mb-3">
                <input type="text" class="form-control text-white student-username" placeholder="نام کاربری">
            </div>
            <div class="col-sm-3">
                <input type="number" class="form-control text-white student-group" placeholder="شماره گروه">
            </div>                            
        </div>
        `
    }

    formContainer.innerHTML += '<button class="form-group btn btn-primary w-100" id="register-students">ثبت نام دانش آموزان</button>'

    let regBut = document.querySelector('#register-students');
    regBut.addEventListener('click', registeration);
}

function registeration() {
    let regAlarm = document.querySelector('#reg-alarm');
    regAlarm.classList.add('d-none');
    let className = document.querySelector('#class-name').value;
    let grade = document.querySelector('#stu-grade').value;
    let studentsNumber = document.querySelector('#stu-nums').value;
    let defualtPass = document.querySelector('#default-pass').value;

    let group_num = 0
    if(studentsNumber % 3 == 0) {
        group_num = Math.floor(studentsNumber/3)
    }
    else {
        group_num = Math.floor(studentsNumber/3) + 1
    }

    let studentsInfo = []
    let students = document.querySelectorAll('.student-info');
    for(let i = 0; i < students.length; i++) {
        let studentInfo = {}
        let student = students[i];
        let fName = student.querySelector('.student-fname').value;
        let lName = student.querySelector('.student-lname').value;
        let userName = student.querySelector('.student-username').value;
        let group = student.querySelector('.student-group').value;

        if(!fName || !lName || !userName || !group) {
            regAlarm.classList.remove('d-none');
            return;
        }

        studentInfo['fname'] = fName;
        studentInfo['lname'] = lName;
        studentInfo['user_name'] = userName;
        studentInfo['group'] = group;

        studentsInfo.push(studentInfo);

    }



    // let csrf = document.querySelector('#_token').value;
    let csrf = '';
    
    let pigeon = {
        csrfmiddlewaretoken: csrf, 
        students: studentsInfo, 
        class: className,
        grade: grade, 
        quantity: studentsNumber, 
        groups: group_num,
        password: defualtPass
    }
    console.log(pigeon)
    $.ajax({
        type: "POST",
        url: "/get-students",
        data: JSON.stringify(pigeon),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result) {
            if(result['success']) {
                distination = 'http://' + window.location.host + '/teacher'
                window.location.replace(distination)
            }
        }
      });
}