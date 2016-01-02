$(document).ready(function(){
    'use strict'; //http://ejohn.org/blog/ecmascript-5-strict-mode-json-and-more/

    if ($('#gallery_photo_upload').length == 0) {
        return;
    }

    $('#processing_wait').hide();
    $('#error_text').hide();

    var gallery_id = window.location.pathname.match(/\d+/)[0];

    //Server-side upload handler:
    var url = '/gallery=' + gallery_id + '/upload_images_post/';
    $('#progress .progress-bar').css('width','0%');

    var csrftoken = $("[name='csrfmiddlewaretoken']").val();

    gallery_photo_upload(gallery_id, url, csrftoken);
});


function gallery_photo_upload(gallery_id, url, csrftoken) {

    $('#gallery_photo_upload').fileupload({
        url: url,
        crossDomain: false,
        beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
        dataType: 'json',
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
        maxFileSize: 15000000, // 15 MB
        maxNumberOfFiles: 5,
        limitConcurrentUploads: 3,

        fail: function(e, data){
            $('#processing_wait').hide();
            $('#error_text').show();
        },

        //navigate to tag image once uploaded
        done: function (e, data) {
            var image_id = data.result[0].image_id;

            window.location.href = '/image=' + image_id.toString() + '/details/';
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