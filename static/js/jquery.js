// Ensure jQuery is ready and the DOM has loaded
$(function () {
  //Nav bar active background effect
  $(".menu a").on("click", function () {
    $(this).addClass("active");
  });

  $('#search-focus').on("keypress",function(event){
    if(event.key === "Enter"){
      $("#searchBtn").click(); 
    }
  })
  $("#searchBtn").on("click", function () {
    const inputString = $("#search-focus").val();
    const selectType = $("#data_type").val();
    const column1 = $('#col-1');
    const column2 = $('#col-2');
    const column3 = $('#col-3');
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
          column1.text("Continent(short-form)");
          column2.text("Value(%)");
          column3.text("Location");
        }
        else if(selectType == 'RELATED_QUERIES'){
          column1.text("Queries");
          column2.text("Value(%)");
          column3.hide();
        }
        else if(selectType == 'RELATED_TOPICS'){
          column1.text("Topics");
          column2.text("Topic types");
          column3.text("Value(%)");
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
      for (var key in data[i]) { 
          row += "<td>" + data[i][key] + "</td>";
          //console.log('result:',data[i][key])
        }
      row += "</tr>";
      tableBody.append(row);
      console.log('data:',data)
    }

    // for (var i = 0; i < data.length; i++) {
    //   var row = "<tr>";
    //   if (data[i].location) { 
    //     row += "<td>" + data[i].location + "</td>";
    //     row += "<td>" + data[i].geo + "</td>";
    //     row += "<td>" + data[i].value + "</td>";
    //   } else {  //handle by topics and queries cases
    //     for (var key in data[i]) { //loop through the object through the key to return the values
    //       row += "<td>" + data[i][key] + "</td>";
    //       //console.log('result:',data[i][key])
    //     }
    //   }
    //   row += "</tr>";
    //   tableBody.append(row);
    //   console.log('data:',data)
    // }
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
