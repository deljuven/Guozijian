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

function reanderArea(counts) {
    Morris.Area({
        element: 'morris-area-chart',
        data: genData(counts),
        xkey: 'date',
        ykeys: ['count'],
        labels: ['Count'],
        pointSize: 2,
        hideHover: 'auto',
        resize: true,
        xLabelFormat: function (x) {
            return x.yyyymmmddMMHH();
        }
    });
}

function renderDonut(count) {
    Morris.Donut({
        element: 'morris-donut-chart',
        data: genDonuts(count),
        resize: true
    });
}

function renderBar(counts) {
    Morris.Bar({
        element: 'morris-bar-chart',
        data: genData(counts),
        xkey: 'date',
        ykeys: ['count'],
        labels: ['Count'],
        hideHover: 'auto',
        resize: true
    });
}

function genDonuts(count) {
    return [{label: "识别出的", value: count.count}];
}

function genData(counts) {
    return $.map(counts, function (item) {
        return {date: new Date(item.taken_at).yyyymmmddMMHH(), count: item ? item.count : Math.random() * 100}
    });
}
