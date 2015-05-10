$(document).ready(function() {

    if ($('#image_map').length == 0) {
        return;
    }

    var trans_edit = $('#enable').data('trans_edit');
    var trans_done = $('#enable').data('trans_done');

     //enable / disable
   $('#enable').click(function(e) {

        $('#editable_content .editable').editable('toggleDisabled');
        if ($('#enable').html() == trans_edit) {
           $('#enable').text(trans_done);
        }
        else {
           $('#enable').text(trans_edit);
        }
        e.preventDefault();
	    $('html, body').stop().animate({
	        'scrollTop': $('#enable').offset().top
	    }, 900, 'swing', function () {
	        window.location.hash = $('#enable');
	    });
    });


    $('#title').editable({
        validate: function(value) {
            if(!value) return $('#title').data('trans_required');
        },
        disabled: true
    });


    $('#description').editable({
        disabled: true
    });

    $('#date_taken').editable({
        placement: 'right',
        combodate: {
            firstItem: 'name'
        },
        disabled: true
    });

    $('#latitude').editable({
        disabled: true
    });

    $('#longitude').editable({
        disabled: true
    });

    get_tags();


    $('#tag_detail_modal').on('show.bs.modal', function(e) {
        var person_id = e.relatedTarget.dataset.person_id;
        $("#tag_detail_profile_link").attr("href", "/profile=" + person_id + "/");
        $("#tag_detail_description").html(e.relatedTarget.dataset.person_name);
        $("#tag_detail_delete_button").attr("data-tag_id", e.relatedTarget.dataset.tag_id)
    });

    $("#tag_detail_delete_button").click(function(e) {

        var csrftoken = $.cookie('csrftoken');
        $.ajax({
            url: "/tag=" + e.currentTarget.dataset.tag_id + "/delete/",
            type: "POST",
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (data) {
                var id = "#tag" + data.id.toString();
                $(id).remove();
            },
            error: function (e) {
                var i = e;
            }
        });
    });

    $("#image_map").click(function(e) {
        //http://www.1stwebdesigner.com/image-tagging-tutorial/
        var width = $('#image_map').width();
        var height = $('#image_map').height();
        var left_distance = e.pageX - $(this).offset().left;
        var top_distance = e.pageY - $(this).offset().top;
        var height_diff = 0.03 / height * width;

        $("#tag_add_modal_x1").val(left_distance / width - 0.03);
        $("#tag_add_modal_x2").val(left_distance / width + 0.03);
        $("#tag_add_modal_y1").val(top_distance / height - height_diff);
        $("#tag_add_modal_y2").val(top_distance / height + height_diff);
    });

    //input event only works on IE > 8
    $("#search_text").on('input', function() {
        do_tagging_search();
    });
});

function create_tag(e) {
    // Set the person_id value on the hidden form
    var person_id = e.target.dataset.person_id;
    $("#tag_add_modal_person").val(person_id);

    // Submit it
    var serializedData = $("#tag_add_post").serialize();

    var image_id = $('#image_map').data('id');

    request = $.ajax({
        url: "/image=" + image_id + "/tags/create/",
        dataType: "json",
        type: "post",
        data: serializedData,
    });

    request.done(function (data) {
        var image_position = $('#image_map').position();
        var width = $('#image_map').width();
        var height = $('#image_map').height();
        $('#tag_container').append(create_tag_ui(data, image_position, width, height));
    });
}

function do_tagging_search() {

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

        for (var i in data){
            //Build an array using the data
            var row = ['<tr>'];
            row.push('<td class="search_photo"><a href="/profile=' + data[i].pk + '">');

            if (data[i].fields.small_thumbnail == '' || data[i].fields.small_thumbnail == null){
                row.push('<img src="/static/img/portrait_80.png" ');
            }
            else{
                row.push('<img src="/media/' + data[i].fields.small_thumbnail + '" ');
            }
            row.push('alt="');
            row.push(data[i].fields.name);
            row.push('"/>');
            row.push('</a></td>');
            row.push('<td style="padding-top:40px"><a href="#" class="person_tag_add" data-dismiss="modal" data-person_id ="');
            row.push(data[i].pk);
            row.push('">');
            row.push(data[i].fields.name);
            row.push('</a></td>');
            row.push('</td></tr>');

            //Append it to the table
            $('#results').append(row.join(''));
        }

        $(".person_tag_add").click(function(e) {
           create_tag(e);
        });
    });
}

function get_tags() {

    var image_id = $('#image_map').data('id');

    $.ajax({
        url: "/image=" + image_id + "/tags/get/",
        dataType: "json",
        success: function(data) {

            var image_position = $('#image_map').position();
            var width = $('#image_map').width();
            var height = $('#image_map').height();

            var html =[];
            for (var i in data) {
                html.push(create_tag_ui(data[i], image_position, width, height));
            }
            $('#tag_container').append($(html.join('')));
        }
    });
}

function create_tag_ui(data, image_position, width, height)
{
    var html = [];
    html.push('<a href="#tag_detail_modal" data-toggle="modal" id="tag');
    html.push(data.id);
    html.push('" data-person_id="');
    html.push(data.person);
    html.push('" data-person_name="');
    html.push(data.name);
    html.push('" data-tag_id="');
    html.push(data.id);
    html.push('" class="tag_box" style="left:');
    html.push(data.x1 * width + image_position.left);
    html.push('px;top:');
    html.push(data.y1 * height + image_position.top);
    html.push('px;width:');
    html.push((data.x2 - data.x1) * width);
    html.push('px;height:');
    html.push((data.y2 - data.y1) * height);
    html.push('px">');
    html.push('<div class="tag_description" style="top:');
    html.push((data.y2 - data.y1) * height + 3);
    html.push('px">');
    html.push(data.name)
    html.push('</div>');
    html.push('</a>');
    return html.join('');
}