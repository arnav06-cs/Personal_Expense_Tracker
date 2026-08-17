/*
=========================================
Chart Helper Functions
=========================================
*/

function createPieChart(canvasId, labels, values, colors){

    new Chart(document.getElementById(canvasId),{

        type:"pie",

        data:{

            labels:labels,

            datasets:[{

                data:values,

                backgroundColor:colors

            }]

        },

        options:{

            responsive:true,

            plugins:{

                legend:{
                    position:"bottom"
                }

            }

        }

    });

}


function createBarChart(canvasId, labels, values){

    new Chart(document.getElementById(canvasId),{

        type:"bar",

        data:{

            labels:labels,

            datasets:[{

                label:"Expense",

                data:values

            }]

        },

        options:{

            responsive:true,

            scales:{
                y:{
                    beginAtZero:true
                }
            }

        }

    });

}