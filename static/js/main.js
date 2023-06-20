const algorithms = {
    "random": undefined,
    "exchange:intra": undefined,
    "exchange:inter": undefined,
    "relocate:intra": undefined,
    "relocate:inter": undefined,
    "twoOpt:intra": undefined,
    "tabouSearch": {
        "nbIter": '<input type="number" min="0" name="%p" id="%p" value="500" />',
        "tabouSize": '<input type="number" min="0" name="%p" id="%p" value="30" />',
        "methods": '<select id="%p" name="%p" multiple></select>',
    },
    "annealing": {
        "methods": '<select id="%p" name="%p" multiple></select>',
    },
}


window.addEventListener("load", () => {
    handle_algorithms();

    var graph_base = null;
    var chart = null;
    document.querySelector("#upload").addEventListener("click", () => {
        let formData = new FormData();
        let file = document.querySelector("#file").files[0];
        if (file == undefined) return;
        formData.append("file", file);

        let algo = document.querySelector("#algorithm").value;
        formData.append("algo", algo);
        if (algorithms[algo] !== undefined) {
            for (let param_id of Object.keys(algorithms[algo])) {
                let param = document.querySelector("#" + param_id);
                if (param.type == "select-multiple") {
                    let values = [];
                    for (let option of param.selectedOptions) {
                        values.push(option.value);
                    }
                    formData.append(param_id, JSON.stringify(values));
                } else
                    formData.append(param_id, param.value);
            }
        }
        fetch("/front/create_graph", { method: "POST", body: formData })
            .then((response) => { return response.json(); })
            .then((data) => { graph_base = data; chart = create_graph(graph_base); })
            .catch(() => { return; });
    });

    setInterval(() => {
        if (graph_base == null) return;
        fetch("/front/get_graph", { method: "GET" })
            .then((response) => { return response.json(); })
            .then((data) => { update_graph(chart, data); })
            .catch(() => { return; });
    }, 1000);
});

function create_graph(base) {
    const ctx = document.querySelector("#graph");

    let ids = []
    for (let p of base.clients) {
        ids.push(p.id_name);
    }
    document.querySelector(".clients > p").innerHTML = ids.length;

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
    document.querySelector(".trucks > p").innerHTML = data.routes.length;
    let clients = chart.data.datasets[0];
    chart.data.datasets.length = 0;
    chart.data.datasets.push(clients);
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
            label.innerText = pname.charAt(0).toUpperCase() + pname.slice(1) + " ";
            param.appendChild(label);
            param.innerHTML += phtml.replaceAll("%p", pname);
            if (phtml.includes("select")) {
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