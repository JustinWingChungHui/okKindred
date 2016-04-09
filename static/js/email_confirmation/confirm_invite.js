require(["jquery", "bootstrap", "validator"], function ($) {

    $(document).ready(function() {

        // Initialises the validation on the password box
        $('#inputPassword').validator()

        // Disable form and show overlay if everything is valid on submit
        $('#password_form').validator().on('submit', function (e) {
            if (!e.isDefaultPrevented()) {
                $(this).find("button[type='submit']").prop('disabled',true);
                $('.loading').show();
            }
        });
    });
});

