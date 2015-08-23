$(document).ready(function(){

    //http://stackoverflow.com/questions/11054511/how-to-handle-lack-of-javascript-object-bind-method-in-ie-8


    //input event only works on IE > 8
    $("#search_text").on('input', function() {
        do_search();
    });

    //IE8 Compatibility
    if( $("html").hasClass("ie8") ) {

        //Event does not work on touch screen
        $('#search_text').keyup(function() {
            do_search();
        });
    };


    function do_search() {

        if($('#search_text').val()==null || $('#search_text').val()=="")
        {
            $('#results').html("");
            return false;
        }

        $('#searching_in_progress').show();

        var $form = $("#search_form");

        // Serialize the data in the form
        var serializedData = $form.serialize();


        // Fire off the request
        request = $.ajax({
            url: "/get_search_results_json/",
            dataType: "json",
            type: "post",
            data: serializedData
        });

        // Callback handler that will be called on success
        request.done(function (data){

            //Clear results
            $('#results').html('');
            $('#searching_in_progress').hide();

            var html = [];
            var template = $('#search_person_row').html();

            for (var i in data){
                var data_row = data[i];
                var image_url;

                if (data_row.fields.small_thumbnail == '' || data_row.fields.small_thumbnail == null){
                    image_url = "/static/img/portrait_80.png";
                }
                else{
                    image_url = "/media/" + data[i].fields.small_thumbnail;
                }

                var person = {
                    id :  data_row.pk,
                    name : data_row.fields.name,
                    image_url : image_url
                };

                var output = Mustache.render(template, person);
                html.push(output);
            }

            $('#results').append(html.join(''));
        });
    }

});