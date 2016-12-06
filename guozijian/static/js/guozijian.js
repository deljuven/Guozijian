function snapshot() {
    $.get("snapshot", function (data) {
        alert(data.title);
    });
}

function ping() {
    console.log("ping");
}

function queryParams() {
    return {
        per_page: 5,
        page: 1
    };
}

function loadCounts(params) {
    $.get("counts", function (data) {
        params.success({
            "total": data.total,
            "rows": data.data
        });
    });
}

$(document).ready(function () {
    $('#table').on('click-cell.bs.table', function (field, value, row, element) {
        $("#gallery").attr("src", element.uri);
    });
});