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
    let tabs = document.querySelectorAll('.nav-link');
    for(let i = 0; i < tabs.length - 1; i++) {
        tabs[i].addEventListener('click', showTab);
    }
}

function showTab(e) {
    let tab = e.target;
    let tabId = tab.getAttribute('href')

    let selectedTab = document.querySelector(tabId);
    let radios = selectedTab.querySelectorAll('.form-check-input');
    for(let i = 0; i < radios.length; i++) {
        radios[i].addEventListener('click', loadContent)
    }

}

function loadContent(e) {
    let item = e.target;
    let mainDiv = item.parentElement.parentElement;
    let section = mainDiv.parentElement.getAttribute('id');
    let video = document.querySelector('#orig-' + section);
    let deaf = document.querySelector('#deaf-' + section);
    let text = document.querySelector('#text-' + section);
    let contentDiv = mainDiv.querySelector('#content-container');
    
    if(item.value == 1) {
        deaf.classList.add('d-none');
        text.classList.add('d-none');
        video.classList.remove('d-none');
    }
    else if(item.value == 2) {
        text.classList.add('d-none');
        video.classList.add('d-none');
        deaf.classList.remove('d-none');
    }
    else if(item.value == 3) {
        video.classList.add('d-none');
        deaf.classList.add('d-none');
        text.classList.remove('d-none');
    }
}


