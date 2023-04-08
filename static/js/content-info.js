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
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const sit = urlParams.get('sit');
    console.log(sit)
    let notFound = document.querySelector('#not-found-text');
    if(sit) {
        notFound.classList.remove('d-none');
    }
    else {
        notFound.classList.add('d-none');
    }
   
    let start = document.querySelector('#start-btn');
    start.addEventListener('click', getContentInfo)
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

