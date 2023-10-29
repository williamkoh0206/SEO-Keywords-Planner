// Ensure jQuery is ready and the DOM has loaded
$(function () {
  //Nav bar active background effect
  $(".menu a").on("click", function () {
    $(this).addClass("active");
  });

  $("#searchBtn").on("click", function () {
    const inputString = $("#search-focus").val();
    const selectType = $("#data_type").val();
    const column1 = $('#col-1');
    const column2 = $('#col-2');
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
        if (selectType == 'GEO_MAP_0'){
          $("#col-1").text("Location");
          $("#col-2").text("Value");
        }
        else if(selectType == 'RELATED_QUERIES'){
          $("#col-1").text("Queries");
          $("#col-2").text("Value");
        }
        else if(selectType == 'RELATED_TOPICS'){
          $("#col-1").text("Topics");
          $("#col-2").text("Value");
        }
      },
    });
    $("#search-focus").val("");
  });
  function displayResults(data) {
    var tableBody = $("#searchResultsTable tbody");
    tableBody.empty();

    for (var i = 0; i < data.length; i++) {
      var row = "<tr>";
      if (data[i].location) { //handle by topic and keywords case
        row += "<td>" + data[i].location + "</td>";
        row += "<td>" + data[i].value + "</td>";
      } else { //handle by region case
        for (var key in data[i]) {
          row += "<td>" + data[i][key] + "</td>";
        }
      }
      row += "</tr>";
      tableBody.append(row);
    }
  }
});
