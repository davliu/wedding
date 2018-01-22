$(function() {
  var showPlusOne = function() {
    if ($("#plus_one").is(":checked")) {
      $(".plus-one-field").show("fast");
    } else {
      $(".plus-one-field").hide("fast");
    }
  };

  var changeAttending = function() {
    var isAttending = $("#attending").is(":checked");
    $(":input").each(function() {
      var input = $(this);
      if (
        ["hidden", "submit", "button"].indexOf(input.attr("type")) != -1 ||
        input.attr("id") == "attending"
      ) {
        return;
      }
      input.prop("disabled", !isAttending);
    });
  };

  $("#plus_one").on("change", function() {
    showPlusOne();
  });
  $("#attending").on("change", function() {
    changeAttending();
  });

  showPlusOne();
  changeAttending();
}());
