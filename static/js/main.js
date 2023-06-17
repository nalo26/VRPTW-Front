const algorithms = {
    "random": undefined,
    "exchange/intra": undefined,
    "exchange/inter": undefined,
    "relocate/intra": undefined,
    "relocate/inter": undefined,
    "twoOpt/intra": undefined,
    "tabouSearch": {
        "nbIter": '<input type="number" min="0" name="%p" id="%p" default="500" />',
        "tabouSize": '<input type="number" min="0" name="%p" id="%p" default="30" />',
        "methods": '<select id="%p" name="%p" multiple>%o</select>',
    },
    "annealing": {
        "methods": '<select id="%p" name="%p" multiple>%o</select>',
    },
}


window.addEventListener("load", () => {
    handle_algorithms();

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

function handle_algorithms() {
    let dropdown = document.querySelector("#algorithm");
    for (let algo in algorithms) {
        let option = document.createElement("option");
        option.setAttribute('value', algo);
        option.innerText = algo;
        dropdown.appendChild(option);
    }
    document.querySelector("#algorithm").addEventListener("change", e => {
        let algo = e.target.value;
        let algo_params = algorithms[algo];
        let params = document.querySelector("#params");
        params.innerHTML = "";
        if (algo_params == undefined) return;
        for (let [pname, phtml] of Object.entries(algo_params)) {
            let param = document.createElement("div");
            param.classList.add("param");
            let label = document.createElement("label");
            label.setAttribute("for", pname);
            label.innerText = pname.charAt(0).toUpperCase() + pname.slice(1);
            param.appendChild(label);
            param.innerHTML += phtml.replaceAll("%p", pname);
            if (phtml.includes("%o")) {
                for (let a_name of Object.keys(algorithms).slice(0, -2)) {
                    let option = document.createElement("option");
                    option.setAttribute('value', a_name);
                    option.innerText = a_name;
                    param.querySelector("select").appendChild(option);
                }
            }
            params.appendChild(param);
        }
    });
}