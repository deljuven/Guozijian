function snapshot() {
    $.get("snapshot", function (data) {
        alert(data.title);
    });
}

function ping() {
    console.log("ping");
}

function queryParams(){
    return {
        per_page: 5,
        page: 1
    };
}

$(document).ready(function () {
    // $('#dataTable').dataTable({
    //     "bPaginate": true,
    //     "iDisplayLength": 5,
    //     "bLengthChange": false,
    //     "bFilter": true,
    //     "bInfo": false,
    //     "bAutoWidth": true });
});