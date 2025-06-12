$(document).ready(function () {
    function stock_form_update() {
        let $fromLocation = $('#stock_update_form #id_from_location');
        let $toLocation = $('#stock_update_form #id_to_location');

        let typeValue = $('#stock_update_form #id_type').val();
        let locationValue = $('#stock_update_form #initial_location').val();

        switch(typeValue){
            case 'I':
                // clear and hide origin location
                $fromLocation.val('');
                $fromLocation.parent().hide();
                $fromLocation.find('option').show();

                // set, show and disable destination location
                $toLocation.val(locationValue);
                $toLocation.find('option').show();
                $toLocation.find('option:not(:selected)').hide();
                $toLocation.parent().show();
                break;
            case 'O':
                // set, show and disable origin location
                $fromLocation.val(locationValue);
                $fromLocation.parent().show();
                $fromLocation.find('option').show();
                $fromLocation.find('option:not(:selected)').hide();

                // clear and hide destination location
                $toLocation.val('');
                $toLocation.parent().hide();
                $toLocation.find('option').show();
                break;
            case 'T':
                // set, show and disable origin location
                $fromLocation.val(locationValue);
                $fromLocation.parent().show();
                $fromLocation.find('option').show();
                $fromLocation.find('option:not(:selected)').hide();

                // show and enable origin location, clear if same value, hide same location value option
                if ($toLocation.val() === locationValue) $toLocation.val('');
                $toLocation.parent().show();
                $toLocation.find('option').show();
                $toLocation.find('option[value="' + locationValue + '"]').hide();
                break;
        }
    }
    stock_form_update();
    $('#stock_update_form .form-text').hide();
    $('#stock_update_form #id_product').find('option:not(:selected)').hide();
    $('#stock_update_form #id_type').on('change', stock_form_update);
})