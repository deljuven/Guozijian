bootstrap_alert = function () {
}
bootstrap_alert.warning = function (message) {
    $('#alert_placeholder').html('<div class="alert alert-warning" role="alert"><a class="close" data-dismiss="alert">×</a><span>' + message + '</span></div>')
}

function snapshot(class_id) {
    $.get("snapshot", {'class': class_id}, function (data) {
        if (data.err)
            bootstrap_alert.warning(data.err)
        location.reload();
    });
}

var donut, bar, area;

function loadCounts(params) {
    $.get("counts", params.data).done(function (data) {
        params.success({
            total: data.total,
            rows: data.data
        });
        var max_height = Math.max($("#img_list").height(), $("#gallery").height());
        $("#img_list").height(max_height);
        $("#gallery").height(max_height);
    });
    var donut_params = params.data;
    donut_params['last'] = 3;
    delete donut_params['offset'];
    delete donut_params['limit'];
    $.get("counts", donut_params).done(function (data) {
        if (data.data.length > 0) {
            if (bar) {
                bar.setData(genData(data.data));
            } else
                bar = renderBar(data.data, 'morris-bar-chart');
            if (area) {
                area.setData(genData(data.data));
            } else
                area = reanderArea(data.data, 'morris-area-chart');
            if (donut) {
                donut.setData(genDonuts(data.data[0], total));
            } else {
                donut = renderDonut(data.data[0], 'morris-donut-chart', total);
            }
            donut.select(0);
            var max_height = Math.max($("#morris-bar-chart").height(), $("#morris-donut-chart").height());
            $("#morris-bar-chart").height(max_height);
            $("#morris-donut-chart").height(max_height);
        }
        var max_height = Math.max($("#img_list").height(), $("#gallery").height());
        $("#img_list").height(max_height);
        $("#gallery").height(max_height);
    });
}

function refreshTable() {
    $('#table').bootstrapTable('refresh', {silent: true});
}

$(document).ready(function () {
    $('#table').on('click-cell.bs.table', function (field, value, row, element) {
        $("#gallery").attr("src", element.uri);
        if (donut) {
            donut.setData(genDonuts(element, total));
            donut.select(0);
        }
        var max_height = Math.max($("#img_list").height(), $("#gallery").height());
        $("#img_list").height(max_height);
        $("#gallery").height(max_height);
    });

    onMessage("/msg_refresh", refreshTable);
});