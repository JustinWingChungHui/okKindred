
//The build will inline common dependencies into this file.
// Use multiple CDNs because of Chinese Firewall
requirejs.config({
    "baseUrl": '/static/js',
    "paths": {
        jquery : [
                "//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min",
                "//ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min",
                "//cdn.jsdelivr.net/jquery/3.2.1/jquery.min",
                "node_modules/jquery/dist/jquery.min"
                ],

        bootstrap : [
                "//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min",
                "//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min",
                "//cdn.jsdelivr.net/bootstrap/3.3.7/js/bootstrap.min",
                "node_modules/bootstrap/dist/js/bootstrap.min"
                ],

        mustache : [
                "//cdnjs.cloudflare.com/ajax/libs/mustache.js/2.3.0/mustache.min",
                "//cdn.jsdelivr.net/mustache.js/2.3.0/mustache.min",
                "node_modules/mustache/mustache.min"
                ],

        underscore : [
                    "//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min",
                    "//fastcdn.org/Underscore.js/1.8.3/underscore-min",
                    "node_modules/underscore/underscore.min"
                    ],

        jsPlumb : [
                    "//cdnjs.cloudflare.com/ajax/libs/jsPlumb/2.2.10/jsplumb.min",
                    "node_modules/jsplumb/dist/js/jsplumb.min"
                    ],

        moment : [
                "//cdnjs.cloudflare.com/ajax/libs/moment.js/2.18.1/moment.min",
                "//cdn.jsdelivr.net/momentjs/2.18.1/moment.min",
                "node_modules/moment/min/moment.min"
                ],

        validator: [
                "//cdnjs.cloudflare.com/ajax/libs/1000hz-bootstrap-validator/0.11.9/validator.min",
                "node_modules/bootstrap-validator/dist/validator.min"
                ],

        bootstrap_editable : [
                            "//cdnjs.cloudflare.com/ajax/libs/x-editable/1.5.1/bootstrap3-editable/js/bootstrap-editable.min",
                            "//cdn.jsdelivr.net/bootstrap.editable/1.5.1/js/bootstrap-editable.min",
                            "node_modules/x-editable/dist/bootstrap3-editable/js/bootstrap-editable.min"
                            ],

        leaflet : [
                    "//cdnjs.cloudflare.com/ajax/libs/leaflet/1.0.3/leaflet",
                    "//cdn.jsdelivr.net/leaflet/1.0.3/leaflet",
                    "node_modules/leaflet/dist/leaflet"
                    ],

        leaflet_markercluster : [
                                "//cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.0.6/leaflet.markercluster",
                                "//cdn.jsdelivr.net/leaflet.markercluster/1.0.5/leaflet.markercluster",
                                "node_modules/leaflet.markercluster/dist/leaflet.markercluster"
                                ],

        jquery_fileupload : [
                            "//cdnjs.cloudflare.com/ajax/libs/blueimp-file-upload/9.18.0/js/jquery.fileupload.min",
                            "node_modules/blueimp-file-upload/js/jquery.fileupload"
                            ],

        jquery_cookie : [
                        "//cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.min",
                         "node_modules/jquery.cookie/jquery.cookie"
                        ],

        'jquery-ui/ui/widget' : [
                            "/static/js/libs/jquery.widget.min"
                            ],

        jcrop : [
                "//cdnjs.cloudflare.com/ajax/libs/jquery-jcrop/2.0.4/js/Jcrop.min",
                "bower_components/Jcrop/js/Jcrop.min"
                ],

        tinymce: [
                "//cdnjs.cloudflare.com/ajax/libs/tinymce/4.6.4/tinymce.min",
                "node_modules/tinymce/tinymce.min"
                ],

        mobile : "/static/js/common/mobile",

        masonry : [
                    "//cdnjs.cloudflare.com/ajax/libs/masonry/4.2.0/masonry.pkgd.min",
                    "//cdn.jsdelivr.net/masonry/4.2.0/masonry.pkgd.min",
                    "node_modules/masonry-layout/dist/masonry.pkgd.min"
                    ],

        photoswipe : [
                    "//cdnjs.cloudflare.com/ajax/libs/photoswipe/4.1.2/photoswipe.min",
                    "//cdn.jsdelivr.net/photoswipe/4.1.2/photoswipe.min",
                    "node_modules/photoswipe/dist/photoswipe.min"
                    ],

        photoswipe_ui : [
                        "//cdnjs.cloudflare.com/ajax/libs/photoswipe/4.1.2/photoswipe-ui-default.min",
                        "//cdn.jsdelivr.net/photoswipe/4.1.2/photoswipe-ui-default.min",
                        "node_modules/photoswipe/dist/photoswipe-ui-default.min"
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
        },

        leaflet_markercluster : {
            deps : ['leaflet']
        },
    }
});

// Makes sure bootstrap is loaded for all pages so normal drop downs and modals work
require(["jquery", "bootstrap"], function ($) {

    // Fallover to local copy of bootstrap css if CDN fails, repeat base styles to override bootstrap
    if ($('#bootstrapCssTest').is(':visible') === true) {
        $('<link href="/static/js/libs/node_modules/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet" type="text/css" /> <link rel="stylesheet" type="text/css" href="/static/css/base.css"/>').appendTo('head');
    }
});


