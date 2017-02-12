require(["jquery", "jquery_cookie", "jquery_fileupload"], function ($) {

    $(document).ready(function(){
        'use strict'; //http://ejohn.org/blog/ecmascript-5-strict-mode-json-and-more/

        if ($('#profile_picture_upload').length == 0) {
            return;
        }

        $('#processing_wait').hide();
        $('#error_text').hide();

        var person_id = window.location.pathname.match(/\d+/)[0];

        //Server-side upload handler:
        var url = '/image_upload=' + person_id + '/';
        $('#progress .progress-bar').css('width','0%');

        var csrftoken = $("[name='csrfmiddlewaretoken']").val();

        set_profile_picture_upload(person_id, url, csrftoken);

    });

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }


    function set_profile_picture_upload(person_id, url, csrftoken) {

        // Upload the photos

        $('#profile_picture_upload').fileupload({
            url: url,
            crossDomain: false,
            maxNumberOfFiles: 1,
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            dataType: 'json',
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
            maxFileSize: 15000000, // 15 MB

        }).on('fileuploadfail', function(e, data){
                $('#processing_wait').hide();
                $('#error_text').show();

        }).on('fileuploaddone', function (e, data) {
                //navigate to resize image once uploaded
                //Pull the id from the url
                window.location.href = '/image_resize=' + person_id + '/';

        }).on('fileuploadprogressall', function (e, data) {
                //Show uploading status
                var progress = parseInt(data.loaded / data.total * 100, 10);
                $('#progress .progress-bar').css(
                    'width',
                    progress + '%'
                );

                if (progress >= 100) {
                     $('#processing_wait').show();
                }

        }).prop('disabled', !$.support.fileInput)
            .parent().addClass($.support.fileInput ? undefined : 'disabled');
    }

});