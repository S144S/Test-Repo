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
    let submitBut = document.querySelector('#submit-setting');
    submitBut.addEventListener('click', submitSetting);
}

function submitSetting() {
    let corpFail = document.querySelector('#setting-fail');
    let cityFail = document.querySelector('#city-empty');
    // let alarm = document.querySelector('#enable-alarm').checked;
    let corp = document.querySelector('#corp-type').value;
    let city = document.querySelector('#city').value;

    cityFail.classList.add('d-none');
    corpFail.classList.add('d-none');

    if(corp == 0) {
        corpFail.classList.remove('d-none');
        return;
    }

    if(city == 0) {
        cityFail.classList.remove('d-none');
        return;
    }

    let pigeon = {
        alarm: 1, 
        city: city,
        corp: corp
    }
    console.log(pigeon)
    $.ajax({
        type: "POST",
        url: "/api/setting",
        data: JSON.stringify(pigeon),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result) {
            if(result['status']) {
                let distination = 'http://' + window.location.host
                console.log(distination)
                window.location.replace(distination)
            }
        }
      });
    


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