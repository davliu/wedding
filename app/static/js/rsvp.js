$(function() {
  var showPlusOne = function() {
    if ($("#has_plus_one").is(":checked")) {
      $(".plus-one").show();
    } else {
      $(".plus-one").hide();
    }
  };

  $("#has_plus_one").on("change", function() {
    showPlusOne();
  });

  showPlusOne();
}())
