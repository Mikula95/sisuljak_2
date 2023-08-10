document.addEventListener("DOMContentLoaded", function() {
    const buttons = ['btnA1', 'btnA2', 'btnA3', 'btnB1', 'btnB2'];
    buttons.forEach(btn => {
        document.getElementById(btn).addEventListener("click", function() {
            fetchAnswer(btn.replace('btn', ''));
        });
    });
});

function fetchAnswer(question) {
    fetch(`/calculate/${question}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            const resultElem = document.getElementById(`result${question}`);

            if (['A1', 'B1', 'B2'].includes(question)) {
                resultElem.innerText = data.result;
            } else if (['A2', 'A3'].includes(question)) {
                const tableBody = resultElem.querySelector('tbody');
                tableBody.innerHTML = '';

                data.result.forEach(row => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${row.Gn}</td>
                        <td>${row.mean || row.Percentile || 'N/A'}</td>
                        <td>${row.std || ''}</td>
                    `;
                    tableBody.appendChild(tr);
                });
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
}


$(document).ready(function() {
    $("#btnB2").click(function() {
        $.get("/calculate_b2", function(data) {
            var meanTableBody = $("#resultA2 tbody");
            var stdTableBody = $("#resultA3 tbody");

            meanTableBody.empty();
            stdTableBody.empty();

            data.mean_table.forEach(row => {
                var tr = $("<tr>")
                    .append($("<td>").text(row.Gn))
                    .append($("<td>").text(row.mean))
                    .append($("<td>").text(row.mean_percentile));
                meanTableBody.append(tr);
            });

            data.std_table.forEach(row => {
                var tr = $("<tr>")
                    .append($("<td>").text(row.Gn))
                    .append($("<td>").text(row.std))
                    .append($("<td>").text(row.std_percentile));
                stdTableBody.append(tr);
            });
        });
    });
});
