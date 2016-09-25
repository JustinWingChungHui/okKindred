require(["jquery", "bootstrap_editable", "bootstrap"], function ($) {

    //turn to inline mode
    $.fn.editable.defaults.mode = 'inline';
    $.fn.editable.defaults.showbuttons = false;
    $.fn.editable.defaults.onblur = 'submit';

    $(document).ready(function() {

        var required_text = $('#translation').data('required');

        $('#name').editable({
            validate: function(value) {
                if(!value) return required_text;
            }
        });


        $('#gender').editable({
            validate: function(value) {
                if(!value) return required_text;
            },
        });

        $('#language').editable({
            validate: function(value) {
                if(!value) return required_text;
            },
        });

        $('#email').editable();
        $('#birth_year').editable();
        $('#year_of_death').editable();
        $('#telephone_number').editable();
        $('#website').editable();
        $('#address').editable();
        $('#skype_name').editable();
        $('#facebook').editable();
        $('#twitter').editable();
        $('#linkedin').editable();
        $('#occupation').editable();
        $('#spoken_languages').editable();

        var no = $('#translation').data('no');
        var yes = $('#translation').data('yes');

        //Pass through an empty string for false
        $('#locked').editable({
            source: [
                        {value: 0, text: no},
                        {value: 1, text: yes },
                    ],
        });
    });
});