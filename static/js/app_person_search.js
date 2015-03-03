$(document).ready(function(){

    //input event only works on IE > 9
    $("#search_form").bind('input', function() {

        if($('#search_text').val()==null || $('#search_text').val()=="")
        {
            $('#results').html("");
            return false;
        }

        $('#searching_in_progress').show();

        var $form = $(this);

        // Serialize the data in the form
        var serializedData = $form.serialize();


            // Fire off the request to /form.php
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

            for (var i in data){
                //Build an array using the data
                var row = ['<tr>']
                row.push('<td class="search_photo"><a href="/profile=' + data[i].pk + '">');

                if (data[i].fields.small_thumbnail == '' || data[i].fields.small_thumbnail == null){
                    row.push('<img src="/static/img/smiley_80.jpg" ');
                }
                else{
                    row.push('<img src="/media/' + data[i].fields.small_thumbnail + '" ');
                }
                row.push('alt="' + data[i].fields.name +'"')
                row.push('/>');
                row.push('</a></td>');
                row.push('<td style="padding-top:40px"><a href="/profile=' + data[i].pk + '">' + data[i].fields.name);
                row.push('</a></td>');
                row.push('</td></tr>');

                //Append it to the table
                $('#results').append(row.join(''));
            }

        });

    });

});