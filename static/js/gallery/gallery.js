
var gallery_page = 0;
var gallery_loading = false;

//Request the galleries on page load
$( document ).ready(function() {
    //Initiate  masonry
    var $container = $('#image_container');

    if ($container.length == 0) {
        return;
    }

    $container.imagesLoaded(function(){
        $container.masonry({
            itemSelector: '.image_in_gallery',
            columnWidth: 1,
            isFitWidth: true
        });
    });

    //Display the default image if there is one
    if ($('#default_image').length > 0) {
        $('#default_image').trigger('click');
    }

    gallery_load_more();
});


//Request more galleries when we scroll to the bottom
$(window).scroll(function()
{
    if ($('#image_container').length == 0) {
        return;
    }

    if($(window).scrollTop() > $(document).height() - $(window).height() - 100)
    {
        gallery_load_more();
    }
});

//Ajax request to get more galleries
function gallery_load_more()
{
    if (gallery_loading == true) { return; }

    gallery_loading = true;

    gallery_page = gallery_page + 1;

    var gallery_url = $('#image_container').data('gallery_url');

    $('div#loadmoreajaxloader').show();
    $.ajax({
        url: gallery_url + gallery_page.toString(),
        success: function(data) {
            if(data && data.length > 0) {

                var template = $('#galley_image_template').html();

                var html =[];
                var show_map = false;
                for (var i in data) {
                    var data_row = data[i];

                    var image_data = {
                      id :   data_row.pk,
                      title : data_row.fields.title,
                      thumbnail : data_row.fields.thumbnail,
                      large_thumbnail : data_row.fields.large_thumbnail
                    };

                    var output = Mustache.render(template, image_data);
                    html.push(output);

                    if (data_row.fields.latitude != 0) {
                        show_map = true;;
                    }

                }

                if (show_map == true) {
                    $('#map_button').show();
                }
                $('div#loadmoreajaxloader').hide();

                var $data = $(html.join(''));
                var $container = $('#image_container');
                $container.append($data).imagesLoaded(function(){
                    $container.masonry( 'appended', $data.filter(".image_in_gallery"), true );

                    gallery_loading = false;

                    //Keep loading images until we see a scroll bar
                    if ($container.height() < $(window).height()) {
                        gallery_load_more()
                    }
                });
            }
            else {
                $('#NoMoreImages').show();
                $('div#loadmoreajaxloader').hide();
            }
        },

        error: function(jqXHR, textStatus, errorThrown ) {
            $('#ErrorLoadingImages').show();
            $('div#loadmoreajaxloader').hide();
            gallery_loading = false;
        }
    });
}