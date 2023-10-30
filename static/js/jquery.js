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
    const headerColumn = $('#searchResultsTable tr');
    console.log(inputString);

    $.ajax({
      url: "/search",
      type: "GET",
      data: { keyword: inputString, type: selectType },
      beforeSend: function () {
        // Show the loading effect
        showLoadingEffect();
      },
      success: function (response) {
        displayResults(response);
        const originalText = "Keyword results for";
        $("#keywordValue").text(originalText + " " + inputString);
        headerColumn.removeClass()
        $("#searchResultsTable").show();
        if (selectType == 'GEO_MAP_0'){
          $("#col-1").text("Location");
          $("#col-2").text("Value(%)");
        }
        else if(selectType == 'RELATED_QUERIES'){
          $("#col-1").text("Queries");
          $("#col-2").text("Value(%)");
        }
        else if(selectType == 'RELATED_TOPICS'){
          $("#col-1").text("Topics");
          $("#col-2").text("Value(%)");
        }
      },
      complete: function () {
        // Hide the loading effect
        removeLoadingEffect();
      },
      error: function(){

      }
    });
    //$("#search-focus").val("");
  });
  function displayResults(data) {
    var tableBody = $("#searchResultsTable tbody");
    tableBody.empty();

    for (var i = 0; i < data.length; i++) {
      var row = "<tr>";
      if (data[i].location) { //handle by region case location key
        row += "<td>" + data[i].location + "</td>";
        row += "<td>" + data[i].value + "</td>";
      } else {  //handle by topics and queries cases
        for (var key in data[i]) { //loop through the object through the key to return the values
          row += "<td>" + data[i][key] + "</td>";
          //console.log('result:',data[i][key])
        }
      }
      row += "</tr>";
      tableBody.append(row);
      //console.log('data:',data)
    }
  }
    // Show the loading effect
    function showLoadingEffect() {
      $('#loadingEffect').removeClass('d-none');
    }
      // Hide the loading effect
    function removeLoadingEffect() {
    $("#loadingEffect").addClass('d-none');
  }
});
