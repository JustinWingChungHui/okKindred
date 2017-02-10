
//The build will inline common dependencies into this file.
// Use multiple CDNs because of Chinese Firewall
requirejs.config({
    "baseUrl": '/static/js/libs',
    "paths": {
        jquery : [
                "//cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min",
                "//ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min",
                "bower_components/jquery/dist/jquery.min"
                ],

        bootstrap : [
                "//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min",
                "//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min",
                "bower_components/bootstrap/dist/js/bootstrap.min"
                ],

        mustache : [
                "//cdnjs.cloudflare.com/ajax/libs/mustache.js/2.3.0/mustache.min",
                "//cdn.jsdelivr.net/mustache.js/2.3.0/mustache.min",
                "bower_components/mustache.js/mustache.min"
                ],

        underscore : [
                    "//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min",
                    "//fastcdn.org/Underscore.js/1.8.3/underscore-min",
                    "bower_components/underscore/underscore.min"
                    ],

        jsPlumb : [
                    "//cdnjs.cloudflare.com/ajax/libs/jsPlumb/2.2.10/jsplumb.min",
                    "bower_components/jsplumb/dist/js/jsplumb.min"
                    ],

        moment : [
                "//cdnjs.cloudflare.com/ajax/libs/moment.js/2.17.1/moment.min",
                "bower_components/moment/min/moment.min"
                ],

        validator: [
                "//cdnjs.cloudflare.com/ajax/libs/1000hz-bootstrap-validator/0.11.9/validator.min",
                "bower_components/bootstrap-validator/dist/validator.min"
                ],

        bootstrap_editable : [
                            "//cdnjs.cloudflare.com/ajax/libs/x-editable/1.5.1/bootstrap3-editable/js/bootstrap-editable.min",
                            "bower_components/x-editable/dist/bootstrap3-editable/js/bootstrap-editable.min"
                            ],

        // Breaking changes do later...
        leaflet : [
                    "//cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/leaflet",
                    "//cdn.jsdelivr.net/leaflet/0.7.7/leaflet",
                    "bower_components/leaflet/dist/leaflet"
                    ],

        jquery_fileupload : [
                            "//cdnjs.cloudflare.com/ajax/libs/blueimp-file-upload/9.15.0/js/jquery.fileupload.min",
                            "bower_components/blueimp-file-upload/js/jquery.fileupload"
                            ],

        jquery_cookie : [
                        "//cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.min",
                         "bower_components/jquery.cookie/jquery.cookie"
                        ],

        'jquery-ui/ui/widget' : [
                            "/static/js/libs/jquery.widget.min"
                            ],

        jcrop : [
                "//cdnjs.cloudflare.com/ajax/libs/jquery-jcrop/2.0.4/js/Jcrop.min",
                "bower_components/Jcrop/js/Jcrop.min"
                ],

        tinymce: [
                "//cdnjs.cloudflare.com/ajax/libs/tinymce/4.5.3/tinymce.min",
                "bower_components/tinymce/tinymce.min"
                ],

        mobile : "/static/js/common/mobile",

        masonry : [
                    "//cdnjs.cloudflare.com/ajax/libs/masonry/4.1.1/masonry.pkgd.min",
                    "//cdn.jsdelivr.net/masonry/4.1.1/masonry.pkgd.min",
                    "bower_components/masonry/dist/masonry.pkgd.min"
                    ],

        photoswipe : [
                    "//cdnjs.cloudflare.com/ajax/libs/photoswipe/4.1.1/photoswipe.min",
                    "//cdn.jsdelivr.net/photoswipe/4.1.1/photoswipe.min",
                    "bower_components/photoswipe/dist/photoswipe.min"
                    ],

        photoswipe_ui : [
                        "//cdnjs.cloudflare.com/ajax/libs/photoswipe/4.1.1/photoswipe-ui-default.min",
                        "//cdn.jsdelivr.net/photoswipe/4.1.1/photoswipe-ui-default.min",
                        "bower_components/photoswipe/dist/photoswipe-ui-default.min"
                        ],

    },
    "shim": {
        underscore: {
            exports: "_"
        },

        /* Set bootstrap dependencies (just jQuery) */
        bootstrap : {
            deps : ['jquery'],
        },

        moment: {
            noGlobal: false
        },

        bootstrap_editable : {
            deps : ['bootstrap', "moment"]
        },

        validator : {
             deps : ['jquery', 'bootstrap']
        },

        /* Set jquery ui dependencies*/
        'jquery-ui/ui/widget' : {
            deps : ['jquery']
        },

        jquery_cookie : {
            deps : ['jquery']
        },


        jsPlumb : {
            exports : "jsPlumb"
        },

        jcrop : {
            deps : ['jquery']
        },

        tinymce : {
            exports : "tinymce"
        }
    }
});

// Makes sure bootstrap is loaded for all pages so normal drop downs and modals work
require(["jquery", "bootstrap"], function ($) {

    // Fallover to local copy of bootstrap css if CDN fails, repeat base styles to override bootstrap
    if ($('#bootstrapCssTest').is(':visible') === true) {
        $('<link href="/static/js/libs/bower_components/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet" type="text/css" /> <link rel="stylesheet" type="text/css" href="/static/css/base.css"/>').appendTo('head');
    }
});


