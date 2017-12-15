$(function() {
  var showPlusOne = function() {
    if ($("#plus_one").is(":checked")) {
      $(".plus-one").show();
    } else {
      $(".plus-one").hide();
    }
  };

  $("#plus_one").on("change", function() {
    showPlusOne();
  });

  showPlusOne();
}())
