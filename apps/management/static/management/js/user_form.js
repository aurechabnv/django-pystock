$(document).ready(function () {
    let $id_is_staff = $('#id_is_staff')
    let $id_companies = $('#id_companies')

    // If `is_staff` is checked, `companies` field must be hidden
    $id_is_staff.change(function() {
        $id_companies.parent().css('display', this.checked?'none':'block');
    });

    // Hide `companies` field on initialisation if necessary
    if ($id_is_staff.is(':checked')) {
        $id_companies.parent().hide();
    }
})