require(["jquery"], function ($) {

    $(document).ready(function() {

        if ($('#invite_submit').length == 0) {
            return;
        }

        $("#invite_submit").click(function(e) {

            $('#invite_in_progress').show();

            var $form = $('#invite_with_email_form'); //Require whole form to include csrf token
            var serializedData = $form.serialize();

            var person_id = $('#invite_with_email_form').data('person_id');

            // Fire off the request to update email
            request = $.ajax({
                url: "/update_person=" + person_id + "/",
                type: "post",
                data: serializedData,
                success: function(data) {
                    // Submit form if update successful
                    $('#invite_form').submit();
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    $('#invite_in_progress').hide();
                    $('#email_error').html(xhr.responseText);
                }
            });
        });
    });
});