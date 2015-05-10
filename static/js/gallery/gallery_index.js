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

                var last_updated = $("#translation").data("lastupdated");
                var html =[];

                for (var i in data) {
                    html.push('<tr class="gallery_index_row">');
                    html.push('<td>');
                    html.push('<a href="/gallery=');
                    html.push(data[i].pk.toString());

                    if (data[i].fields.thumbnail) {
                        html.push('"><img class="gallery_index_thumbnail" src="/media/' + data[i].fields.thumbnail + '" ');
                    }
                    else {
                        html.push('"><img class="gallery_index_thumbnail" src="/static/img/gallery_thumb.jpg" ');
                    }

                    html.push('alt="' + data[i].fields.title +'/"')
                    html.push('/></a></td>');

                    html.push('<td>');
                    html.push('<a href="/gallery=');
                    html.push(data[i].pk.toString());
                    html.push('"><h4>');
                    html.push(data[i].fields.title);
                    html.push('</h4><p>');
                    html.push(data[i].fields.description);
                    html.push('</p><p>');
                    html.push(last_updated);
                    html.push(data[i].fields.last_updated_date);
                    html.push('</p></a></td><td>');
                    html.push('</td></tr>');
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