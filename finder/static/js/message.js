function onMessage(url, args, event, on_success) {
    // var socket = io.connect(url);
    var socket = io(url);
    socket.connect(url);
    socket.on('connect', function () {
        console.info('connect');
        if (args){
            socket.emit('join', args);
        }
    });
    socket.on(event, function (data, fun) {
        if (on_success)
            on_success();
        fun();
    });
    socket.on('disconnect', function () {
        console.info('disconnect');
    });
}