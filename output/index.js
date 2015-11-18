$(document).ready(function () {
  "use strict";
  var $table = $('table.schedule');
  // Get Hatena Bookmark count
  $(".hateb-link").each(function (i, item) {
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
