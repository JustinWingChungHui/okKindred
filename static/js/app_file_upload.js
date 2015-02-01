        var person_id = window.location.pathname.match(/\d+/)[0];

        /*jslint unparam: true */
        /*global window, $ */
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $(function () {
            'use strict';
            // Change this to the location of your server-side upload handler:
            var url = '/image_upload=' + person_id + '/';
            $('#progress .progress-bar').css(
                        'width',
                        '0%'
                    );
            $('#processing_wait').hide();
            $('#error_text').hide();

            var csrftoken = $.cookie('csrftoken');
            $('#fileupload').fileupload({
                url: url,
                crossDomain: false,
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type)) {
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

                    //TODO Display Error messages
                 },


                //Show uploading status
                progressall: function (e, data) {
                    var progress = parseInt(data.loaded / data.total * 100, 10);
                    $('#progress .progress-bar').css(
                        'width',
                        progress + '%'
                    );

                    if (progress >= 100) {
                         $('#processing_wait').show()
                    }

                }
            }).prop('disabled', !$.support.fileInput)
                .parent().addClass($.support.fileInput ? undefined : 'disabled');

        });