require(["jquery", "bootstrap", "validator", "bootstrap_editable"], function ($) {

        //turn to inline mode
        $.fn.editable.defaults.mode = 'inline';
        $.fn.editable.defaults.url ='/accounts/update_settings/';
        $.fn.editable.defaults.showbuttons = false;
        $.fn.editable.defaults.onblur = 'submit';

        $(document).ready(function() {

            // Initialises the validation on the password box
            $('#password_change').validator()

            var required = $("#translation_settings").data('required');
            $('#language').editable({
                validate: function(value) {
                    if(!value) return required;
                },
            });

            var yes = $("#translation_settings").data('yes');
            var no = $("#translation_settings").data('no');


            //Pass through an empty string for false
            $('#receive_update_emails').editable({
                source: [
                            {value: '', text: no},
                            {value: 1, text: yes},
                        ],
            });

            $('#receive_photo_update_emails').editable({
                source: [
                            {value: '', text: no},
                            {value: 1, text: yes},
                        ],
            });

        });
});

