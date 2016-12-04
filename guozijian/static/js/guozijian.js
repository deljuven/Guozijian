function snapshot() {
    $.get("snapshot", function (data) {
        alert(data.title);
    });
}

function ping() {
    console.log("ping");
}