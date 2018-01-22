$(function() {
  var showPlusOne = function() {
    if ($("#plus_one").is(":checked")) {
      $(".plus-one-field").show("fast");
    } else {
      $(".plus-one-field").hide("fast");
    }
  };

  $("#plus_one").on("change", function() {
    showPlusOne();
  });

  showPlusOne();
}());
