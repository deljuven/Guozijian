bootstrap_alert = function() {}
bootstrap_alert.warning = function(message) {
    $('#alert_placeholder').html('<div class="alert alert-warning" role="alert"><a class="close" data-dismiss="alert">×</a><span>'+message+'</span></div>')
}

function snapshot(class_id) {
    $.get("snapshot", {'class': class_id}, function (data) {
        if (data.err)
            bootstrap_alert.warning(data.err)
        location.reload();
    });
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
            donut.select(0);
        }
    });
}

$(document).ready(function () {
    $('#table').on('click-cell.bs.table', function (field, value, row, element) {
        $("#gallery").attr("src", element.uri);
        donut.setData(genDonuts(element, total));
        donut.select(0);
    });
});