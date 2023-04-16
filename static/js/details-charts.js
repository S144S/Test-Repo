$(function () {
    'use strict';
    var xLabel = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        '10', '11', '12', '13', '14', '15', '16', '17', 
        '18', '19','20', '21', '22', '23'
    ]
    var tempInitData = [];
    var humInitData = [];
    var pressInitData = [];
    var luxInitData = [];

    $.ajax({
        type: "get",
        url: "/api/chart/update",
        async: false,
        success: function(result) {
            tempInitData = result['temp'];
            humInitData = result['hum'];
            pressInitData = result['press'];
            luxInitData = result['lux'];
        }
    })

    var sampleData = [
        10, NaN, 10.5, 11, 13, 14, 15, 16, 10, 11, 12, 20,
        13, 11, 20.2, 13, 16, 16, 16, 14, 40, 30, 20, 22
    ]
    /*=========================================
    Charts
    ===========================================*/
    //===== Temperature chart =====//
    var tempArea = document.getElementById("temp-chart").getContext("2d");
    var tempChart = new Chart(tempArea, {
        type: 'line',
        data: {
            labels: xLabel,
            datasets: [{
                label: 'دما',
                data: tempInitData,
                // spanGaps: true,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }],
        },
        options: {
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    //===== Humidity chart =====//
    var humArea = document.getElementById("hum-chart").getContext("2d");
    var humChart = new Chart(humArea, {
        type: 'line',
        data: {
            labels: xLabel,
            datasets: [{
                label: 'رطوبت',
                data: humInitData,
                // spanGaps: true,
                backgroundColor: 'rgba(24, 156, 222, 0.2)',
                borderColor: 'rgba(24, 156, 222, 1)',
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    //===== Pressues chart =====//
    var pressArea = document.getElementById("press-chart").getContext("2d");
    var pressChart = new Chart(pressArea, {
        type: 'line',
        data: {
            labels: xLabel,
            datasets: [{
                label: 'فشار',
                data: pressInitData,
                // spanGaps: true,
                backgroundColor: 'rgba(24, 222, 103, 0.2)',
                borderColor: 'rgba(24, 222, 103, 1)',
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    //===== Pressues chart =====//
    var luxArea = document.getElementById("lux-chart").getContext("2d");
    var luxChart = new Chart(luxArea, {
        type: 'line',
        data: {
            labels: xLabel,
            datasets: [{
                label: 'نور',
                data: luxInitData,
                // spanGaps: true,
                backgroundColor: 'rgba(222, 215, 24, 0.2)',
                borderColor: 'rgba(222, 215, 24, 1)',
                borderWidth: 1
            }]
        },
        options: {
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

    setInterval(function() {
        $.ajax({
            type: "get",
            url: "/api/chart/update",
            success: function(result) {
                var tempData = result['temp'];
                var humData = result['hum'];
                var pressData = result['press'];
                var luxData = result['lux'];

                tempChart.data.datasets[0].data = tempData;
                humChart.data.datasets[0].data = humData;
                pressChart.data.datasets[0].data = pressData;
                luxChart.data.datasets[0].data = luxData;

                tempChart.update();
                humChart.update();
                pressChart.update();
                luxChart.update();
            }
        })
    }, 10000);
});
