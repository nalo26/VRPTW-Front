window.addEventListener("load", () => {
    document.querySelector("#upload").addEventListener("click", () => {
        let file = document.querySelector("#file").files[0];
        let formData = new FormData();

        formData.append("file", file);
        fetch("/front/create_graph", { method: "POST", body: formData });
    });
});