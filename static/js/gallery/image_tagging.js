var ImageTagging = {}; // globa object container
ImageTagging.Tags = [];

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
           $('#address_search_form').show();
        }
        else {
           $('#enable').text(trans_edit);
           $('#address_search_form').hide();
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

        var csrftoken = $("[name='csrfmiddlewaretoken']").val();
        $.ajax({
            url: "/tag=" + e.currentTarget.dataset.tag_id + "/delete/",
            type: "POST",
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (data) {
                var id = "#tag" + data.id.toString();
                $(id).remove();

                // Remove from cached array
                var i = 0;
                for (var i in ImageTagging.Tags) {
                    var row = ImageTagging.Tags[i];
                    if (row.id == data.id) {
                        break;
                    }
                    i++;
                }
                ImageTagging.Tags.splice(i, 1);
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
        $('#results').html('');
        $("#search_text").val("");
    });

    var timer;
    var delay = 600; // 0.6 seconds delay after last input

    //input event only works on IE > 8
    $("#search_text").on('input', function() {
        window.clearTimeout(timer);
        timer = window.setTimeout(function(){
              //delayed input change action/event
              do_tagging_search();
        }, delay);

    });

    $("#tag_add_modal").on('shown.bs.modal', function() {
        $("#search_text").focus();
    });
});

$(window).resize(function () {
    redraw_tags();
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

    request.done(function (row) {
        var image_position = $('#image_map').position();
        var width = $('#image_map').width();
        var height = $('#image_map').height();
        var template = $('#tag_template').html();

        var tag ={
                id : row.id,
                person : row.person,
                name : row.name,
                left : row.x1 * width + image_position.left,
                top : row.y1 * height + image_position.top,
                width : (row.x2 - row.x1) * width,
                height : (row.y2 - row.y1) * height,
                description_top : (row.y2 - row.y1) * height + 3
        };

        var output = Mustache.render(template, tag);
        $('#tag_container').append(output);

        ImageTagging.Tags.push(row);
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

        var template = $('#search_person_row').html();
        html =[];

        for (var i in data){

            var row = data[i];
            var image_url;

            if (row.fields.small_thumbnail == '' || row.fields.small_thumbnail == null){
                image_url = "/static/img/portrait_80.png";
            }
            else{
                image_url = "/media/" + data[i].fields.small_thumbnail;
            }

            var person = {
                id : row.pk,
                name : row.fields.name,
                image_url : image_url
            };

            var output = Mustache.render(template, person);
            html.push(output);
        }
        $('#results').append(html.join(''));

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
            ImageTagging.Tags = data;
            redraw_tags();
        }
    });
}

function redraw_tags() {
    $(".tag_box").remove();
    var image_position = $('#image_map').position();
    var width = $('#image_map').width();
    var height = $('#image_map').height();

    var html =[];
    var template = $('#tag_template').html();

    for (var i in ImageTagging.Tags) {
        var row = ImageTagging.Tags[i];

        var tag ={
            id : row.id,
            person : row.person,
            name : row.name,
            left : row.x1 * width + image_position.left,
            top : row.y1 * height + image_position.top,
            width : (row.x2 - row.x1) * width,
            height : (row.y2 - row.y1) * height,
            description_top : (row.y2 - row.y1) * height + 3
        };

        var output = Mustache.render(template, tag);
        html.push(output);
    }
    $('#tag_container').append(html.join(''));
}

