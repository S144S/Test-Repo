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
    try {$('#waitingModal').modal({backdrop: 'static'});}
    catch {}
    try {
        $('#waitingModal').modal('hide');
        $('#chestModal').modal({backdrop: 'static'});
    }
    catch {}
    try {
        $('#waitingModal').modal('hide');
        $('#doneAllModal').modal({backdrop: 'static'});
    }
    catch {}
    
    let submitBut = document.querySelector('#submit-resposne');
    submitBut.addEventListener('click', submitResult);

    let nextLevelBut = document.querySelector('#next-level');
    nextLevelBut.addEventListener('click', nextLevel);

}

function submitResult() {
    let response = document.querySelector('#response-val').value;
    let emptyErr = document.querySelector('#resposne-empty');
    let islandId = document.querySelector('#island-id').value;
    let level = document.querySelector('#level-id').innerHTML;

    emptyErr.classList.add('d-none');
    if(!response) {
        emptyErr.classList.remove('d-none');
        return;
    }

    let pigeon = {
        island_id: islandId,
        level: level,
        response: response
    }

    $.ajax({
        type: "POST",
        url: "/submit-answer",
        data: JSON.stringify(pigeon),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result) {
            if(result['status'] == 'pass') {
                $('#passModal').modal({backdrop: 'static'});
            }
            else if(result['status'] == 'complete') {
                $('#completeModal').modal({backdrop: 'static'});
            }
            else if(result['status'] == 'failed') {
                $('#failedModal').modal('show');
            }
        }
      });
}

function nextLevel() {
    location.reload();
    window.scrollTo(0, 0);
}

