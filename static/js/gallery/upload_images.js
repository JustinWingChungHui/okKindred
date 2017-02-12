require(["jquery", "mustache", "jquery_cookie", "jquery_fileupload"], function ($, Mustache) {

    var UPLOAD_STATE = {
        total: 0,
        filename: "",
        image_ids: []
    };

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
            sequentialUploads: true,
            beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    UPLOAD_STATE.total = settings.originalFiles.length;
                    UPLOAD_STATE.filename = settings.files[0].name;
                },
            dataType: 'json',
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
            maxFileSize: 15000000, // 15 MB
            limitConcurrentUploads: 1

        }).on('fileuploadfail', function(e, data){
                UPLOAD_STATE.uploaded++;
                var template = $('#failed_upload').html();
                var output = Mustache.render(template, UPLOAD_STATE);
                $("#progress_text").append(output);

                $('#processing_wait').hide();
                $('#error_text').show();

        }).on('fileuploaddone', function (e, data) {
                //navigate to tag image once uploaded
                UPLOAD_STATE.uploaded++;

                var template = $('#successful_upload').html();
                var output = Mustache.render(template, UPLOAD_STATE);
                 $("#progress_text").append(output);

                 var image_id = data.result[0].image_id;
                 UPLOAD_STATE.image_ids.push(image_id);

                if (UPLOAD_STATE.image_ids.length >= UPLOAD_STATE.total) {
                    window.location.href = '/image=' + UPLOAD_STATE.image_ids[0].toString() + '/details/';
                }

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