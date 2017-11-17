Date.prototype.yyyymmdd = function () {
    var mm = this.getMonth() + 1; // getMonth() is zero-based
    var dd = this.getDate();

    return this.getFullYear() + "-" +
        (mm > 9 ? '' : '0') + mm + "-" +
        (dd > 9 ? '' : '0') + dd;
};

Date.prototype.yyyymmmddMMHH = function () {
    var mm = this.getMonth() + 1; // getMonth() is zero-based
    var dd = this.getDate();
    var HH = this.getHours();
    var MM = this.getMinutes() + 1;

    return this.getFullYear() + "-" +
        (mm > 9 ? '' : '0') + mm + "-" +
        (dd > 9 ? '' : '0') + dd + " " +
        (HH > 9 ? '' : '0') + HH + ":" +
        (MM > 9 ? '' : '0') + MM;
};

function reanderArea(counts, id) {
    return Morris.Area({
        element: id,
        data: genData(counts),
        xkey: 'date',
        ykeys: ['count'],
        labels: ['Count'],
        pointSize: 2,
        hideHover: 'auto',
        resize: true,
        parseTime: false,
        // xLabelFormat: function (x) {
        //     return x.yyyymmmddMMHH();
        // }
    });
}

function renderDonut(count, id, total) {
    return Morris.Donut({
        element: id,
        data: genDonuts(count, total),
        resize: true
    });
}

function renderBar(counts, id) {
    return Morris.Bar({
        element: id,
        data: genData(counts),
        xkey: 'date',
        ykeys: ['count'],
        labels: ['Count'],
        hideHover: 'auto',
        resize: true,
    });
}

function genDonuts(count, total) {
    return [{label: "识别出", value: count.count}, {label: "未识别出", value: total - count.count}];
}

function genData(counts) {
    return $.map(counts, function (item) {
        var value = {date: new Date(item.taken_at).yyyymmmddMMHH(), count: item ? item.count : Math.random() * 100};
        return value;
    });
}
