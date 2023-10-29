// Ensure jQuery is ready and the DOM has loaded
$(function () {
  //Nav bar active background effect
  $(".menu a").on("click", function () {
    $(this).addClass("active");
  });

  $("#searchBtn").on("click", function () {
    const inputString = $("#search-focus").val();
    const selectType = $("#data_type").val();
    console.log(inputString);
    $.ajax({
      url: "/search",
      type: "GET",
      data: { keyword: inputString, type: selectType },
      success: function (response) {
        displayResults(response);
        const originalText = "Keyword results for";
        $("#keywordValue").text(originalText + " " + inputString);
        $("#searchResultsTable").show();
      },
    });
    $("#search-focus").val("");
  });
  function displayResults(data) {
    var tableBody = $("#searchResultsTable tbody");
    tableBody.empty();

    for (var i = 0; i < data.length; i++) {
      let row = "<tr>";
      row += "<td>" + data[i].location + "</td>";
      row += "<td>" + data[i].value + "</td>";
      row += "</tr>";
      tableBody.append(row);
    }
  }
});
