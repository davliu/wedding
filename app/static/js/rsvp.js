$(function() {
  var showPlusOne = function() {
    if ($("#plus_one").is(":checked")) {
      $(".plus-one-field").show();
    } else {
      $(".plus-one-field").hide();
    }
  };

  $("#plus_one").on("change", function() {
    showPlusOne();
  });

  showPlusOne();
}())
