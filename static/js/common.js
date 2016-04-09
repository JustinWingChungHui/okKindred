
//The build will inline common dependencies into this file.

//For any third party dependencies, like jQuery, place them in the lib folder.

//Configure loading modules from the lib directory,
//except for 'app' ones, which are in a sibling
//directory.

//http://stackoverflow.com/questions/13464846/loading-bootstrap-from-cdn-with-require-js
//http://stackoverflow.com/questions/10815454/how-does-requirejs-work-with-multiple-pages-and-partial-views


// Use multiple CDNs because of Chinese Firewall
requirejs.config({
    //"baseUrl": 'static/js',
    "paths": {
        jquery : [
                "//cdnjs.cloudflare.com/ajax/libs/jquery/2.2.2/jquery.min",
                "//ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min",
                ],

        bootstrap : [
                "//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.6/js/bootstrap.min",
                "//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min"
                ],

        mustache : [
                "//cdnjs.cloudflare.com/ajax/libs/mustache.js/2.2.1/mustache.min",
                "//cdn.jsdelivr.net/mustache.js/2.2.1/mustache.min"
                ],

        underscore : "//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min",

        jsPlumb : "//cdnjs.cloudflare.com/ajax/libs/jsPlumb/2.0.7/jsPlumb.min",

        moment : "//cdnjs.cloudflare.com/ajax/libs/moment.js/2.12.0/moment.min",

        validator: "//cdnjs.cloudflare.com/ajax/libs/1000hz-bootstrap-validator/0.10.1/validator.min",

        bootstrap_editable : "//cdnjs.cloudflare.com/ajax/libs/x-editable/1.5.1/bootstrap3-editable/js/bootstrap-editable.min",

        leaflet : "//cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/leaflet",

        jquery_ui : "//cdnjs.cloudflare.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min",

        jquery_fileupload : "//cdnjs.cloudflare.com/ajax/libs/blueimp-file-upload/9.12.1/js/jquery.fileupload.min",

        jquery_cookie : "//cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.min",

        jcrop : "//cdnjs.cloudflare.com/ajax/libs/jquery-jcrop/0.9.12/js/jquery.Jcrop.min",

        tinymce: [
                "//cdnjs.cloudflare.com/ajax/libs/tinymce/4.3.8/tinymce.min",
                "//cdn.tinymce.com/4/tinymce.min"
                ]

    },
    "shim": {
        underscore: {
            exports: "_"
        },

        /* Set bootstrap dependencies (just jQuery) */
        bootstrap : {
            deps : ['jquery'],
        },

        bootstrap_editable : {
            deps : ['jquery', 'bootstrap']
        },

        validator : {
             deps : ['jquery', 'bootstrap']
        },

        /* Set jquery ui dependencies*/
        jquery_ui : {
            deps : ['jquery']
        },
        jquery_fileupload : {
            deps : ['jquery_ui']
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
});


