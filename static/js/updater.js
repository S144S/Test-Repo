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
    setInterval(function() {
        $.ajax({
            type: "get",
            url: "/api/update",
            success: function(result) {update_data(result)}
        })
    }, 30000);
}

function update_data(result) {
    // console.log(result)
    let temperature = document.querySelector("#data-temperature");
    let humidity = document.querySelector("#data-humidity");
    let pressure = document.querySelector("#data-pressure");
    let light = document.querySelector("#data-light");
    let rain = document.querySelector("#data-rain");
    let soil = document.querySelector("#data-soil");
    let date = document.querySelector("#data-date");
    let time = document.querySelector("#data-time");
    let charge = document.querySelector("#data-charge");

    // charge.innerHTML = '<span class="mx-2">تومان</span>';
    // console.log(charge)

    date.innerHTML = result['last_update_date'];
    time.innerHTML = result['last_update_time'];

    temperature.innerHTML = result['temperature'] + ' درجه';
    humidity.innerHTML = result['humidity'] + '%';
    pressure.innerHTML = result['pressure'] + ' پاسکال';
    light.innerHTML = result['light'] + ' لوکس';

    rainData = parseInt(result['rain']);
    soilData = parseInt(result['soil']);
    if(rainData < 1) {
        rain.innerHTML = 'خشک';
    }
    else if(rainData < 2) {
        rain.innerHTML = 'شبنم';
    }
    else if(rainData < 2) {
        rain.innerHTML = 'آرام';
    }
    else {
        rain.innerHTML = 'شدید';
    }

    if(soilData < 1) {
        soil.innerHTML = 'خشک';
    }
    else if(soilData < 2) {
        soil.innerHTML = 'کمی مرطوب';
    }
    else if(soilData < 2) {
        soil.innerHTML = 'نسبتا مرطوب';
    }
    else {
        soil.innerHTML = 'کاملا مرطوب';
    }

}

