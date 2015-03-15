 $(document).ready(function() {

    $("input:radio").change(relation_toggle_slide);

    new_relation_validate();
    $('#input_new_name').bind('input',new_relation_validate);


    //input event only works on IE > 8
    $("#input_existing_name").on('input', function() {
        do_relation_search();
    });

    //IE8 Compatibility
    if( $("html").hasClass("ie8") ) {

        //Event does not work on touch screen
        $('#input_existing_name').keyup(function() {
            do_relation_search();
        });
    };


    $(document).on('click',".add_relation_existing_person",add_relation_existing_person);
});


function add_relation_existing_person(e) {
    e.preventDefault();
	var currentId = $(this).attr('id');
    $('#relation_id').val(currentId);
    $("form#add_relation").submit();
}

function relation_toggle_slide() {
       $('#new_person_data').slideToggle("slow");
       $('#existing_person_data').slideToggle("slow");
       $('#relation_submit').slideToggle("slow");

       if ($('#existing_person').val() == 1) {
           $('#existing_person').val("0");
           $('#input_new_name').val($('#input_existing_name').val());
       }
       else {
           $('#existing_person').val("1");
       }
}


function new_relation_validate(){
    if ($('#input_new_name').val().length > 0) {
        $("#relation_submit").prop("disabled", false);
    }
    else {
        $("#relation_submit").prop("disabled", true);
    }
}


function do_relation_search() {

    if($('#input_existing_name').val()==null || $('#input_existing_name').val()=="")
    {
        $('#input_existing_name').html("");
        return false;
    }

    $('#searching_in_progress').show();

    var $form = $('#add_relation'); //Require whole form to include csrf token

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
    request.done(search_result_returned);
}


function search_result_returned(data){

    //Clear results
    $('#results').html('');
    $('#searching_in_progress').hide();

    var this_person_id = document.URL.match(/\d+/g)

    for (var i in data){
        //Build an array using the data
        var row = ['<tr>']
        row.push('<td class="search_photo">');

        if (data[i].fields.small_thumbnail == '' || data[i].fields.small_thumbnail == null){
            row.push('<img src="/static/img/portrait_80.png"/>');
        }
        else{
            row.push('<img src="/media/' + data[i].fields.small_thumbnail + '"/>');
        }

        row.push('</td>');
        row.push('<td style="padding-top:40px"><a href="#" id="' + data[i].pk + '" class="add_relation_existing_person">' + data[i].fields.name);
        row.push('</a></td>');
        row.push('</td></tr>');

        //Append it to the table
        $('#results').append(row.join(''));
    }

}