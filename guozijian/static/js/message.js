$(document).ready(function () {
    var source = new EventSource("/msg");
    source.addEventListener('server_closed', function (e) {
        source.close();
    });
    source.addEventListener('error', function (e) {
        source.close();
    });
    source.onmessage = function (e) {
        console.info(e.data);
    }
});