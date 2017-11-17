function loadIndex(params) {
    $.get("counts", params).done(function (data) {
        if (data.data.length > 0) {
            renderBar(data.data, 'morris-bar-chart');
            reanderArea(data.data, 'morris-area-chart');
            var max_height = Math.max($("#morris-bar-chart").height(), $("#morris-area-chart").height());
            $("#morris-bar-chart").height(max_height);
            $("#morris-area-chart").height(max_height);
        } else {
            $('#last_week').hide();
        }
    });
    delete params['begin'];
    $.get("counts", params).done(function (data) {
        if (data.data.length > 0) {
            renderBar(data.data, 'history-bar-chart');
            reanderArea(data.data, 'history-area-chart');
            var max_height = Math.max($("#history-bar-chart").height(), $("#history-area-chart").height());
            $("#history-bar-chart").height(max_height);
            $("#history-area-chart").height(max_height);
        } else {
            $('#history').val("No Content");
        }
    });
}