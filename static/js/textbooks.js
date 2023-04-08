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
    let buy = document.querySelector('#buy-textbook');
    buy.addEventListener('click', buyTextBook);
}

function buyTextBook() {
    let lowBudget = document.querySelector('#low-budget');
    let noChoose = document.querySelector('#no-choose');
    let textBooks = document.querySelector('#textbook-boxes');
    let checks = textBooks.querySelectorAll('.form-check-input');
    let islandId = document.querySelector('#island-id').value;
    let selectedBooks = []
    let oldItem = []
    for(let i = 0; i < checks.length; i++) {
        if(checks[i].checked) {
            selectedBooks[i] = 1;
        }
        else {
            selectedBooks[i] = 0;
        }
        if(checks[i].disabled) {
            oldItem[i] = 1;
        }
        else {
            oldItem[i] = 0;
        }
    }

    lowBudget.classList.add('d-none');
    noChoose.classList.add('d-node');
    let nothingChoose = selectedBooks.every((element) => element === 0);

    if(nothingChoose) {
        noChoose.classList.remove('d-none');
        return;
    }

    if(JSON.stringify(oldItem) == JSON.stringify(selectedBooks)) {
        noChoose.classList.remove('d-none');
        return;
    }

    let pigeon = {
        island_id: islandId,
        books: selectedBooks
    }

    console.log(pigeon)

    $.ajax({
        type: "POST",
        url: "/buy-textbook",
        data: JSON.stringify(pigeon),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(result) {
            if(result['status'] == 'done') {
                location.reload();
            }
            else if(result['status'] == 'low') {
                noChoose.classList.add('d-none');
                lowBudget.classList.remove('d-none');
            }
        }
      });
}


