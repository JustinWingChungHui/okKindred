// Disable the submit button to stop double sublmission
$('form').submit(function() {
  $(this).find("button[type='submit']").prop('disabled',true);
});