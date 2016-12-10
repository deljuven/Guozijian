function snapshot(class_id) {
    $.get("snapshot", {'class': class_id}, function (data) {
        alert(data.title);
    });
}

function ping() {
    console.log("ping");
}

function loadCounts(params) {
    $.get("counts", params.data).done(function (data) {
        if (data.data.length > 0) {
            renderBar(data.data);
            reanderArea(data.data);
            renderDonut(data.data[0]);
        }
        params.success({
            total: data.total,
            rows: data.data
        })
    });
}

$(document).ready(function () {
    $('#table').on('click-cell.bs.table', function (field, value, row, element) {
        $("#gallery").attr("src", element.uri);
    });
});