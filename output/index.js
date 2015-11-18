$(document).ready(function () {
  "use strict";
  var $table = $('table.schedule');
  // Get Hatena Bookmark count
  _.each($(".hateb-link"), function (item) {
    var $item = $(item);
    var url = $item.data("url");
    if (url === "#" || url === "") { return }
    $.ajax({
      url: "http://api.b.st-hatena.com/entry.count?url=" + $item.data("url"),
      dataType: "jsonp"
    }).done(function (count) {
      $item.html(count + " Users");
    });
  });
});
