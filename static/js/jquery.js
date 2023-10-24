  // Ensure jQuery is ready and the DOM has loaded
$(function() {
  $(".menu a").on("click", function () {
      $(this).addClass('active');
  });
});