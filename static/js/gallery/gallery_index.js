require(["jquery", "mustache"], function ($, Mustache) {

    var gallery_index_page = 0;
    var gallery_index_loading = false;

    //Request the galleries on page load
    $( document ).ready(function() {

        if ($("#gallery_container").length == 0) {
            return;
        }

        load_more_galleries();
    });


    //Request more galleries when we scroll to the bottom
    $(window).scroll(function()
    {
        if ($("#gallery_container").length == 0) {
            return;
        }

        if($(window).scrollTop() == $(document).height() - $(window).height())
        {
            load_more_galleries();
        }
    });

    //Ajax request to get more galleries
    function load_more_galleries()
    {
        if (gallery_index_loading == true) { return; }

        gallery_index_page = gallery_index_page + 1;
        loading = true;
        $('div#loadmoreajaxloader').show();
        $.ajax({
            url: "/gallery/gallery_data=" + gallery_index_page.toString(),
            success: function(data) {

                if(data && data.length > 0) {

                    var html =[];
                    var template = $('#gallery_row_template').html();

                    for (var i in data) {

                        var row = data[i];

                        var gallerythumb_url;
                        if (data[i].fields.thumbnail) {
                            gallerythumb_url = data[i].fields.thumbnail;
                        }
                        else {
                            gallerythumb_url = "/static/img/gallery_thumb.jpg";
                        }

                        var gallery_row = {
                            id : row.pk,
                            gallerythumb_url : gallerythumb_url,
                            title : row.fields.title,
                            description : row.fields.description,
                            last_updated_date : row.fields.last_updated_date
                        };

                        var output = Mustache.render(template, gallery_row);
                        html.push(output);

                    }

                    $("#gallery_container").append(html.join(''));
                    $('div#loadmoreajaxloader').hide();

                    gallery_index_loading = false;

                    //Keep loading images until we see a scroll bar
                    if ($('#container').height() < $(window).height()) {
                        load_more_galleries()
                    }
                }

                else {
                    $('#no_more_galleries').show();
                    $('div#loadmoreajaxloader').hide();
                }
            }
        });
    }
});