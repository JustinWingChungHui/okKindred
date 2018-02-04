
//The build will inline common dependencies into this file.
// Use multiple CDNs because of Chinese Firewall
requirejs.config({
    "baseUrl": '/static/js',
    "paths": {
        jquery : [
                "//cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min",
                "//cdn.jsdelivr.net/npm/jquery@3.3.1/dist/jquery.min",
                "node_modules/jquery/dist/jquery.min"
                ],

        bootstrap : [
                "//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min",
                "//cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min",
                "node_modules/bootstrap/dist/js/bootstrap.min"
                ],

        mustache : [
                "//cdnjs.cloudflare.com/ajax/libs/mustache.js/2.3.0/mustache.min",
                "//cdn.jsdelivr.net/npm/mustache@2.3.0/mustache.min",
                "node_modules/mustache/mustache.min"
                ],

        underscore : [
                    "//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min",
                    "//cdn.jsdelivr.net/npm/underscore@1.8.3/underscore.min",
                    "node_modules/underscore/underscore.min"
                    ],

        jsPlumb : [
                    "//cdnjs.cloudflare.com/ajax/libs/jsPlumb/2.6.6/js/jsplumb.min",
                    "//cdn.jsdelivr.net/npm/jsplumb@2.6.6/dist/js/jsplumb.min",
                    "node_modules/jsplumb/dist/js/jsplumb.min"
                    ],

        moment : [
                "//cdnjs.cloudflare.com/ajax/libs/moment.js/2.20.1/moment.min",
                "//cdn.jsdelivr.net/npm/moment@2.20.1/moment.min",
                "node_modules/moment/min/moment.min"
                ],

        validator: [
                "//cdnjs.cloudflare.com/ajax/libs/1000hz-bootstrap-validator/0.11.9/validator.min",
                "//cdn.jsdelivr.net/npm/bootstrap-validator@0.11.9/js/validator.min",
                "node_modules/bootstrap-validator/dist/validator.min"
                ],

        bootstrap_editable : [
                            "//cdnjs.cloudflare.com/ajax/libs/x-editable/1.5.1/bootstrap3-editable/js/bootstrap-editable.min",
                            "//cdn.jsdelivr.net/npm/x-editable@1.5.1/dist/bootstrap3-editable/js/bootstrap-editable.min",
                            "node_modules/x-editable/dist/bootstrap3-editable/js/bootstrap-editable.min"
                            ],

        leaflet : [
                    "//cdnjs.cloudflare.com/ajax/libs/leaflet/1.3.0/leaflet",
                    "//cdn.jsdelivr.net/npm/leaflet@1.3.0/dist/leaflet-src.min",
                    "node_modules/leaflet/dist/leaflet"
                    ],

        leaflet_markercluster : [
                                "//cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.3.0/leaflet.markercluster",
                                "//cdn.jsdelivr.net/npm/leaflet.markercluster@1.3.0/dist/leaflet.markercluster.min",
                                "node_modules/leaflet.markercluster/dist/leaflet.markercluster"
                                ],

        jquery_fileupload : [
                            "//cdnjs.cloudflare.com/ajax/libs/blueimp-file-upload/9.20.0/js/jquery.fileupload.min",
                            "//cdn.jsdelivr.net/npm/blueimp-file-upload@9.20.0/js/jquery.fileupload.min",
                            "node_modules/blueimp-file-upload/js/jquery.fileupload"
                            ],

        jquery_cookie : [
                        "//cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.min",
                        "//cdn.jsdelivr.net/npm/jquery.cookie@1.4.1/jquery.cookie.min",
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
                "//cdnjs.cloudflare.com/ajax/libs/tinymce/4.7.6/tinymce.min",
                "//cdn.jsdelivr.net/npm/tinymce@4.7.6/tinymce.min",
                "node_modules/tinymce/tinymce.min"
                ],

        mobile : "/static/js/common/mobile",

        masonry : [
                    "//cdnjs.cloudflare.com/ajax/libs/masonry/4.2.1/masonry.pkgd.min",
                    "//cdn.jsdelivr.net/npm/masonry-layout@4.2/dist/masonry.pkgd.min",
                    "node_modules/masonry-layout/dist/masonry.pkgd.min"
                    ],

        photoswipe : [
                    "//cdnjs.cloudflare.com/ajax/libs/photoswipe/4.1.2/photoswipe.min",
                    "//cdn.jsdelivr.net/npm/photoswipe@4.1.2/dist/photoswipe.min",
                    "node_modules/photoswipe/dist/photoswipe.min"
                    ],

        photoswipe_ui : [
                        "//cdnjs.cloudflare.com/ajax/libs/photoswipe/4.1.2/photoswipe-ui-default.min",
                        "//cdn.jsdelivr.net/npm/photoswipe@4.1.2/dist/photoswipe-ui-default.min",
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


