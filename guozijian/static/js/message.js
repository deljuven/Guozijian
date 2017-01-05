function onMessage(url, on_success, on_close, on_err) {
    var source = new EventSource(url);
    if (on_close)
        source.addEventListener('server_closed', on_close);
    else
        source.addEventListener('server_closed', function (e) {
            source.close();
        });
    if (on_err)
        source.addEventListener('error', on_err);
    else
        source.addEventListener('error', function (e) {
            source.close();
        });
    if (on_success) {
        source.addEventListener('message', function (e) {
            console.info("success: " + e.data);
            on_success();
        });
    } else {
        console.info("failed");
    }
}