window.addEventListener("load", () => {
    var graph_base = null;
    document.querySelector("#upload").addEventListener("click", () => {
        let file = document.querySelector("#file").files[0];
        let formData = new FormData();
        formData.append("file", file);
        fetch("/front/create_graph", { method: "POST", body: formData })
            .then((response) => { return response.json(); })
            .then((data) => { graph_base = data; update_graph(graph_base, null); });
    });

    setInterval(() => {
        if (graph_base == null) return;
        fetch("/front/get_graph", { method: "GET" })
            .then((response) => { return response.json(); })
            .then((data) => { update_graph(graph_base, data); })
            .catch(() => { return; });
    }, 1000);
});

function update_graph(base, data) {

}