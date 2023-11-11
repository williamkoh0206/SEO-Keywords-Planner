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
    const inputString = $("#search-focus").val();
    const selectType = $("#data_type").val();
    const column1 = $("#col-1");
    const column2 = $("#col-2");
    const column3 = $("#col-3");
    const headerColumn = $("#searchResultsTable tr");
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
        // displayResults(response);
        const originalText = "Keyword results for";
        $("#keywordValue").text(originalText + " " + inputString);
        headerColumn.removeClass();
        $("#searchResultsTable").show();
        if (Object.prototype.hasOwnProperty.call(response, "error_message")) {
          $("#searchResultsTable").hide();
          var errorMessage = response.error_message;
          var alertHtml =
            '<div class="alert alert-warning" role="alert"><p class="text-center my-2">' +
            errorMessage +
            "</p></div>";
            if ($("#searchResultsTable").next(".alert").length == 0){
              $("#searchResultsTable").after(alertHtml);
            }
        } else {
          hideAlertIfNeeded()
          displayResults(response);
          const originalText = "Keyword results for";
          $("#keywordValue").text(originalText + " " + inputString);
          headerColumn.removeClass();
          $("#searchResultsTable").show();
          if (selectType == "GEO_MAP_0") {
            column1.text("Continent(short-form)");
            column2.text("Location");
            column3.text("Value").show();
          } else if (selectType == "RELATED_QUERIES") {
            column1.text("Queries");
            column2.text("Value(%)");
            column3.hide();
          } else if (selectType == "RELATED_TOPICS") {
            column1.text("Topics");
            column2.text("Types");
            column3.text("Value(%)").show();
          }
          function displayResults(data) {
            var tableBody = $("#searchResultsTable tbody");
            tableBody.empty();
            for (var i = 0; i < data.length; i++) {
              var row = "<tr>";
              const regionKeyList = ['location_in_short','location','continent_value']
              const queriesKeyList = ['queries_title','queries_value']
              const topicKeyList = ['title','type','value']
              if (selectType == 'GEO_MAP_0'){
                for (key in regionKeyList) {
                  row += "<td>" + data[i][regionKeyList[key]] + "</td>";
                  console.log('result:',data[i][key])
                }
              }
              else if(selectType == 'RELATED_QUERIES'){
                for (key in queriesKeyList) {
                  row += "<td>" + data[i][queriesKeyList[key]] + "</td>";
                  console.log('result:',data[i][key])
                }
              }
              else if(selectType == 'RELATED_TOPICS'){
                for (key in topicKeyList) {
                  row += "<td>" + data[i][topicKeyList[key]] + "</td>";
                  console.log('result:',data[i][key])
                }
              }
              row += "</tr>";
              tableBody.append(row);
              //console.log("data:", data);
            }
          }
        }
      },
      complete: function () {
        // Hide the loading effect
        removeLoadingEffect();
      },
      error: function () {},
    });
    //$("#search-focus").val("");
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
