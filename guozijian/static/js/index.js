function loadIndex(params) {
    $.get("counts", params).done(function (data) {
        if (data.data.length > 0) {
            renderBar(data.data, 'morris-bar-chart');
            reanderArea(data.data, 'morris-area-chart');
        } else {
            $('#last_week').hide();
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