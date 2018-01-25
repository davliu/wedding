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

    $("label").each(function() {
      if ($(this).attr("for") == "attending") {
        return;
      }

      if (isAttending) {
        $(this).removeClass("strikethrough");
      } else {
        $(this).addClass("strikethrough");
      }
    });
  };

  var tracks = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
      url: "/track_search?q=%QUERY",
      wildcard: "%QUERY",
      transform: function(response) {
        return response.tracks;
      }
    }
  });

  $(".track-field").each(function() {
    $(this).typeahead({
      hint: true,
      highlight: true,
      minLength: 1
    }, {
      name: 'tracks',
      source: tracks,
      limit: 5
    });
  });

  $("form").on("keyup keypress", function(e) {
    var keyCode = e.keyCode || e.which;
    if (keyCode === 13) {
      e.preventDefault();
      return false;
    }
  });

  $("#plus_one").on("change", function() {
    showPlusOne();
  });
  $("#attending").on("change", function() {
    changeAttending();
  });

  showPlusOne();
  changeAttending();
}());
