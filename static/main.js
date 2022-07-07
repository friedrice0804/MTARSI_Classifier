console.log("I have located the .js file successfully!")

// In case of ajax error:
// Instead of loading the slim version, 
// load the minified version of jQuery in the html page.
////////////////////////////////////////////////////////////////////////////////////////////

$(document).ready(function () {

  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })
  
  $(function () {
    $('[data-toggle="popover"]').popover()
  })

  $('.popover-dismiss').popover({
    trigger: 'focus'
  })

  $("#spinner-div").hide()
  $("#identifyButtonLoading").hide();

  $("#stat-btn").click(function () {//The load button
  $("#spinner-div").show(); //Load button clicked show spinner
  $("#identifyButtonIdle").hide();
  $("#identifyButtonLoading").show();
  });
});
