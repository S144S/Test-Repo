/*!
	* Toasts
	* 
	* 
*/

var finalResult = 0;

if (document.readyState == 'loading') 
{
    document.addEventListener('DOMContentLoaded', main)
} 
else 
{
    main()
}

function main() {
    let submit = document.querySelector('#submit-answers');
    submit.addEventListener('click', submitAnswers);
}

function submitAnswers() {
    let quizTab = document.querySelector('#tab5');
    let options = quizTab.querySelectorAll('.form-check-input');
    let result = [0, 0, 0, 0, 0];
    let correctSum = 0;

    for(let i = 0; i < options.length; i++) {
        let option = options[i]
        
        if(option.checked) {
            let val = options[i].value
            let qId = option.getAttribute('id');
            let respId = '';
            if (qId.includes("qo1-")) {
                respId = '#resp1'
            }
            else if (qId.includes("qo2-")) {
                respId = '#resp2'
            }
            else if (qId.includes("qo3-")) {
                respId = '#resp3'
            }
            else if (qId.includes("qo4-")) {
                respId = '#resp4'
            }
            else if (qId.includes("qo5-")) {
                respId = '#resp5'
            }
            
            let correct = document.querySelector(respId).value

            let question = 0;
            if((i >= 4) && (i < 8)) question = 1;
            else if((i >= 8) && (i < 12)) question = 2;
            else if((i >= 12) && (i < 16)) question = 3;
            else if((i >= 16) && (i < 20)) question = 4;
            // console.log(i, respId, correct, question)
            if(correct == val) {
                result[question] = 1;
                correctSum++;
            }
            else {
                result[question] = -1;
            }
        } 
    }

    showResult(correctSum, result);
}

function showResult(correctNum, asnwers) {
    let resultModal = document.querySelector('#result-modal');
    let summary = resultModal.querySelector('#modal-summary');
    let total = resultModal.querySelector('#modal-q0');
    let q1 = resultModal.querySelector('#modal-q1');
    let q1Text = '';
    let q2 = resultModal.querySelector('#modal-q2');
    let q2Text = '';
    let q3 = resultModal.querySelector('#modal-q3');
    let q3Text = '';
    let q4 = resultModal.querySelector('#modal-q4');
    let q4Text = '';
    let q5 = resultModal.querySelector('#modal-q5');
    let q5Text = '';

    if (correctNum > 3) {
        finalResult = 2;
        summary.classList.add('text-success');
        summary.classList.remove('text-danger');
        summary.classList.remove('text-warning');
        summary.innerText = 'کارت فوق العاده بود';
    }
    else if((correctNum > 1) && (correctNum < 4)) {
        finalResult = 1;
        summary.classList.add('text-warning');
        summary.classList.remove('text-success');
        summary.classList.remove('text-danger');
        summary.innerText = 'خیلی خوب بود ولی میتونستی بهتر باشی';
    }
    else if(correctNum < 2) {
        finalResult = 0;
        summary.classList.remove('text-success');
        summary.classList.remove('text-warning');
        summary.classList.add('text-danger');
        summary.innerText = 'اصلا نگران نباش، با تلاش بیشتر میتونی جبران کنی';
    }

    totalText = 'موفق شدی به ' + correctNum.toString() + ' از 5 سوال جواب درست بدی';
    total.innerText = totalText;
    
    if(asnwers[0] == 1) q1Text = 'سوال 1: کاملا درست';
    else if(asnwers[0] == -1) q1Text = 'سوال 1: نادرست!';
    else q1Text = 'سوال 1: پاسخ ندادی';
    q1.innerText = q1Text;

    if(asnwers[1] == 1) q2Text = 'سوال 2: کاملا درست';
    else if(asnwers[1] == -1) q2Text = 'سوال 2: نادرست!';
    else q2Text = 'سوال 2: پاسخ ندادی';
    q2.innerText = q2Text;

    if(asnwers[2] == 1) q3Text = 'سوال 3: کاملا درست';
    else if(asnwers[2] == -1) q3Text = 'سوال 3: نادرست!';
    else q3Text = 'سوال 3: پاسخ ندادی';
    q3.innerText = q3Text;

    if(asnwers[3] == 1) q4Text = 'سوال 4: کاملا درست';
    else if(asnwers[3] == -1) q4Text = 'سوال 4: نادرست!';
    else q4Text = 'سوال 4: پاسخ ندادی';
    q4.innerText = q4Text;

    if(asnwers[4] == 1) q5Text = 'سوال 5: کاملا درست';
    else if(asnwers[4] == -1) q5Text = 'سوال 5: نادرست!';
    else q5Text = 'سوال 5: پاسخ ندادی';
    q5.innerText = q5Text;

    $('#result-modal').modal('show');
}

function hideModal() {
    $('#result-modal').modal('hide');
}

function finishExam() {
    $('#result-modal').modal('hide');

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    const userId = urlParams.get('user_id');
    const grade = urlParams.get('grade');
    const lesson = urlParams.get('lesson');
    const session = urlParams.get('session');

    let contentId = grade + '-' + lesson + '-' + session;

    let pigeon = {
        id: userId,
        content: contentId,
        res: finalResult
    }

    $.ajax({
        type: "POST",
        url: "/submit-result",
        data: JSON.stringify(pigeon),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result) {
            if(result['success']) {
                let distination = 'http://' + window.location.host + '/home';
                window.location.replace(distination)
            }
            else {
                console.log('ops')
            }
        }
    });
    
}

function getContentInfo() {
    let warning = document.querySelector('#warning-text');
    let notFound = document.querySelector('#not-found-text');
    notFound.classList.add('d-none');
    try {
        var grade = parseInt(document.querySelector('#grade').value);
        var lesson = parseInt(document.querySelector('#lesson').value);
        var session = parseInt(document.querySelector('#session').value);
        warning.classList.add('d-none');
    }
    catch {
        warning.classList.remove('d-none');
    }
    
    if(grade && lesson && session) {
        let userId = document.querySelector('#user-id').value;
        let pigeon = {user_id: userId, grade: grade, lesson: lesson, session: session}
        console.log(pigeon)
        $.ajax({
            type: "POST",
            url: "/get-content-info",
            data: JSON.stringify(pigeon),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(result) {
                if(result['success']) {
                    let queryString = new URLSearchParams(pigeon).toString();
                    distination = 'http://' + window.location.host + '/course?' + queryString;
                    window.location.replace(distination)
                }
                else {
                    notFound.classList.remove('d-none');
                }
            }
        });
    }
    else {
        warning.classList.remove('d-none');
    }
    
}

