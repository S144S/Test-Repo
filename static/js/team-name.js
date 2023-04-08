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
    let teamBut = document.querySelector('#team-name');
    teamBut.addEventListener('click', changeTeamName);
}

function changeTeamName() {
    let teamName = document.querySelector('#new-name').value;
    let nameErr = document.querySelector('#empty-name-err');
    nameErr.classList.add('d-none');

    if(!teamName) {
        nameErr.classList.remove('d-none');
        return;
    }

    let avatar_name = '';
    let avatars = document.querySelectorAll('.avatar-radio');
    for(let i = 0; i < avatars.length; i++) {
        if(avatars[i].checked) {
            avatar_name = avatars[i].id;
        }
    }

    let pigeon = {
        name: teamName,
        avatar: avatar_name
    }

    $.ajax({
        type: "POST",
        url: "/team-name",
        data: JSON.stringify(pigeon),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result) {
            if(result['status'] == 'ok') {
                location.reload();
            }
        }
      });

}

function helpMe() {
    let islandId = document.querySelector('#island-id').value;
    let groupId = document.querySelector('#group-id').value;
    let level = document.querySelector('#level-id').innerHTML;
    let pigeon = {
        island_id: islandId,
        level: level,
        group_id: groupId
    }

    console.log(pigeon)

    $.ajax({
        type: "POST",
        url: "/req-help",
        data: JSON.stringify(pigeon),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result) {
            if(result['status'] == 'done') {
                location.reload();
            }
            else if(result['status'] == 'low') {
                // noChoose.classList.add('d-none');
                // lowBudget.classList.remove('d-none');
            }
        }
      });
}

function removeHelp(e) {
    let selectedHelp = e.target;
    let helpDiv = selectedHelp.parentElement;
    let helpId = helpDiv.querySelector('.help-id').value;
    let pigeon = {
        help_id: helpId
    }
    $.ajax({
        type: "POST",
        url: "/remove-help",
        data: JSON.stringify(pigeon),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result) {
            if(result['status'] == 'done') {
                location.reload();
            }
            else if(result['status'] == 'low') {
                // noChoose.classList.add('d-none');
                // lowBudget.classList.remove('d-none');
            }
        }
      });
}

function makeHelp(e) {
    let theButton = e.target;
    let selectedTeam = theButton.parentElement;
    let teamId = selectedTeam.querySelector('.help_needed-id').value;
    let pigeon = {
        team_id: teamId
    }
    $.ajax({
        type: "POST",
        url: "/make-help",
        data: JSON.stringify(pigeon),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result) {
            if(result['status'] == 'done') {
                location.reload();
            }
            else if(result['status'] == 'low') {
                // noChoose.classList.add('d-none');
                // lowBudget.classList.remove('d-none');
            }
        }
      });
}

function teacherHelp(e) {
    let code = document.querySelector('#teacher-code');
    let warning = document.querySelector('#teacher-code-warn');
    let teacherHelpBut = document.querySelector('#teacher-help');
    let lowBudget = document.querySelector('#teacher-help-low');

    let pigeon = {
        status: 1
    }
    $.ajax({
        type: "POST",
        url: "/teacher-help",
        data: JSON.stringify(pigeon),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result) {
            if(result['status'] == 'done') {
                code.classList.remove('d-none');
                warning.classList.remove('d-none');
                teacherHelpBut.disabled = true;
            }
            else if(result['status'] == 'low') {
                lowBudget.classList.remove('d-none');
            }
        }
      });
}