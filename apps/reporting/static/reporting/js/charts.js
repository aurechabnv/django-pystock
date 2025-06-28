$(document).ready(function () {
    const $myLineChart = $('#myLineChart');
    $.ajax({
        url: $myLineChart.data('url'),
        success: function (json) {
            const data = {
                labels: json.labels,
                datasets: [{
                    label: 'Entrées',
                    data: json.in,
                },{
                    label: 'Sorties',
                    data: json.out,
                },{
                    label: 'Transferts',
                    data: json.tr,
                }]
            };
            const config = {
                type: 'bar',
                data: data,
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                }
            };
            new Chart($myLineChart, config);
        }
    })

    const $myPieChart = $('#myPieChart');
    $.ajax({
        url: $myPieChart.data('url'),
        success: function (json) {
            const data = {
                labels: json.labels,
                datasets: [{
                    label: "Produits",
                    data: json.data,
                }]
            };
            const config = {
                type: 'doughnut',
                data: data,
            };
            new Chart($myPieChart, config);
        }
    })
})