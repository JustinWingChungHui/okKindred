require(["jquery", "tinymce"], function ($, tinymce) {

    var language = $('#biography').data('language');

    tinymce.init({
            selector: 'textarea',
            language_url : '/static/js/tinymce_languages/' + language + '.js',
        });
});