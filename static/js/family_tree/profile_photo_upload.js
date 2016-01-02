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

        fail: function(e, data){
            $('#processing_wait').hide();
            $('#error_text').show();
        },

        //navigate to resize image once uploaded
        done: function (e, data) {
            //Pull the id from the url
            window.location.href = '/image_resize=' + person_id + '/';
         },

        //Show uploading status
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .progress-bar').css(
                'width',
                progress + '%'
            );

            if (progress >= 100) {
                 $('#processing_wait').show();
            }

        }
    }).prop('disabled', !$.support.fileInput)
        .parent().addClass($.support.fileInput ? undefined : 'disabled');
}

