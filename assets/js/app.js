$(function () {
    $('[data-provide="datepicker"]').datetimepicker({
        icons: {
            date: "fa fa-calendar",
            up: "fa fa-arrow-up",
            down: "fa fa-arrow-down"
        },
        format: 'DD/MM/YYYY'
    });
    $('[data-provide="datetimepicker"]').datetimepicker({
        icons: {
            time: "fa fa-clock-o",
            date: "fa fa-calendar",
            up: "fa fa-arrow-up",
            down: "fa fa-arrow-down"
        },
        format: 'DD/MM/YYYY HH:mm'
    });
});
