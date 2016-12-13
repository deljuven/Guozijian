function snapshot(class_id) {
    $.get("snapshot", {'class': class_id}, function (data) {
        location.reload();
    });
}

function ping() {
    console.log("ping");
}

var donut;

function loadCounts(params) {
    $.get("counts", params.data).done(function (data) {
        params.success({
            total: data.total,
            rows: data.data
        })
    });
    var begin = new Date();
    begin.setDate(begin.getDate() - 3);
    params.data['begin'] = begin / 1000;
    $.get("counts", params.data).done(function (data) {
        if (data.data.length > 0) {
            renderBar(data.data, 'morris-bar-chart');
            reanderArea(data.data, 'morris-area-chart');
            donut = renderDonut(data.data[0], 'morris-donut-chart', total);
        }
    });
}

function loadIndex(params) {
    $.get("counts", params).done(function (data) {
        if (data.data.length > 0) {
            renderBar(data.data, 'morris-bar-chart');
            reanderArea(data.data, 'morris-area-chart');
        }
    });
    delete params['begin'];
    $.get("counts", params).done(function (data) {
        if (data.data.length > 0) {
            renderBar(data.data, 'history-bar-chart');
            reanderArea(data.data, 'history-area-chart');
        }
    });
}

$(document).ready(function () {
    $('#table').on('click-cell.bs.table', function (field, value, row, element) {
        $("#gallery").attr("src", element.uri);
        donut.setData(genDonuts(element, total));
    });
});