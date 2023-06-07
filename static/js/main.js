window.addEventListener("load", () => {
    var graph_base = null;
    var chart = null;
    document.querySelector("#upload").addEventListener("click", () => {
        let file = document.querySelector("#file").files[0];
        let formData = new FormData();
        formData.append("file", file);
        fetch("/front/create_graph", { method: "POST", body: formData })
            .then((response) => { return response.json(); })
            .then((data) => { graph_base = data; chart = create_graph(graph_base); });
    });

    setInterval(() => {
        if (graph_base == null) return;
        fetch("/front/get_graph", { method: "GET" })
            .then((response) => { return response.json(); })
            .then((data) => { update_graph(chart, data); })
            .catch(() => { return; });
    }, 500);
});

function create_graph(base) {
    const ctx = document.querySelector("#graph");

    let ids = []
    for (let p of base.clients) {
        ids.push(p.id_name);
    }

    let chart = new Chart(ctx, {
        data: {
            labels: ids,
            datasets: [
                {
                    type: 'scatter',
                    label: 'Clients',
                    data: base.clients,
                }
            ]
        },
        options: {
            animation: {
                duration: 0
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'right',
                }
            }
        }
    });

    return chart;
}

function update_graph(chart, data) {
    document.querySelector(".fitness > p").innerHTML = data.fitness;
    let clients = chart.data.datasets[0];
    chart.data.datasets.length = 0;
    chart.data.datasets.push(clients);
    console.log(chart.data.datasets);
    for (let id = 0; id < data.routes.length; id++) {
        let route_data = {
            type: 'line',
            label: "Route #" + id,
            data: data.routes[id].route,
            tension: 0.1,
            borderColor: [
                'rgba(54, 162, 235, 0.7)',
                'rgba(255, 99, 132, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(255, 159, 64, 0.7)',
                'rgba(153, 102, 255, 0.7)',
                'rgba(255, 205, 86, 0.7)',
            ],
        }
        chart.data.datasets.push(route_data);
    }
    chart.update();
}