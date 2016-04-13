require(["jquery", "jcrop"], function ($) {

    $(function($) {
        $('#crop_target').Jcrop({
            bgColor:     'black',
            bgOpacity:   .4,
            setSelect:   [ 200, 200, 50, 50 ],
            aspectRatio: 1,
            onSelect: updateCoords,
            onChange: updateCoords,
        });
    });

    $.fn.rotate = function(degrees) {
        $(this).css({'-webkit-transform' : 'rotate('+ degrees +'deg)',
                     '-moz-transform' : 'rotate('+ degrees +'deg)',
                     '-ms-transform' : 'rotate('+ degrees +'deg)',
                     'transform' : 'rotate('+ degrees +'deg)'});
        return $(this);
    };

    function updateCoords(c) {
        $('#x').val(c.x);
        $('#y').val(c.y);
        $('#w').val(c.w);
        $('#h').val(c.h);
        $('#display_height').val($('#crop_target').height());
    };

    function checkCoords() {
        if (parseInt($('#w').val())) return true;
            alert('{% trans "Please select a trimmed region" %}');
        return false;
    };
});