$(document).ready(function () {
    $('#id_is_staff').change(function() {
        $('#id_companies').parent().toggle();
    });
})