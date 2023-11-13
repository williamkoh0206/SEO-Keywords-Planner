// Ensure jQuery is ready and the DOM has loaded
$(function () {
  //Nav bar active background effect
  $(".menu a").on("click", function () {
    $(this).addClass("active");
  });

  $("#search-focus").on("keypress", function (event) {
    if (event.key === "Enter") {
      $("#searchBtn").click();
    }
  });

  function hideAlertIfNeeded() {
    if ($("#searchResultsTable").next(".alert").is(":visible")) {
      console.log("being hidden");
      $("#searchResultsTable").next(".alert").remove();
    }
  }

  $("#searchBtn").on("click", function () {
    $('#searchForm').submit();
    showLoadingEffect()
  });
  // Show the loading effect
  function showLoadingEffect() {
    $("#loadingEffect").removeClass("d-none");
  }
  // Hide the loading effect
  function removeLoadingEffect() {
    $("#loadingEffect").addClass("d-none");
  }
});
