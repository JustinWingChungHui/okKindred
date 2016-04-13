// Disable the submit button to stop double submission
require(["jquery"], function ($) {
    $('form').submit(function() {
      $(this).find("button[type='submit']").prop('disabled',true);
      $('.loading').show();
    });
});