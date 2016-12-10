function loadClass(params) {
    $.get("classes/list", params.data).done(function (data) {
        params.success({
            total: data.total,
            rows: data.data
        })
    });
}

function initUpdate(value, row, index) {
    return '<a class="update" title="Update Item"><i class="glyphicon glyphicon-edit"></i></a>';
}

function initDelete(value) {
    return '<a class="remove" title="Delete Item"><i class="glyphicon glyphicon-remove-circle"></i></a>';
}

function onDelete(class_id) {
    $.ajax({
        url: "classes/" + class_id,
        type: 'DELETE',
        success: function (data) {
            console.log(data);
        },
        error: function (data) {
            console.log(data);
        }
    });
    $('#table').bootstrapTable("refresh");
}

$(document).ready(function () {
    $('#table').on('click-cell.bs.table', function (event, row, value, element) {
        if (row == "update" || row == "delete")
            return;
        var redirect_to = "statistic?class=" + element.id;
        window.location.href = redirect_to;
    });

    window.updateEvent = {
        'click .update': function (e, row, value, element) {
            var redirect_to = "classes/" + value.id;
            window.location.href = redirect_to;
        }
    };
    window.deleteEvent = {
        'click .remove': function (e, row, value, element) {
            $('#table').bootstrapTable('remove', {
                field: 'id',
                values: [value.id]
            });
            onDelete(value.id);
        }
    };
});