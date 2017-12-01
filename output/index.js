$(document).ready(function () {
  "use strict";
  var $table = $('table.schedule');
  // Get Hatena Bookmark count
  $(".hateb-link").each(function (i, item) {
    var $item = $(item);
    var url = $item.data("url");
    if (url === "#" || url === "") { return }
    $.ajax({
      url: "https://b.hatena.ne.jp/entry.count",
      data: {
        url: encodeURI(url)
      },
      dataType: "jsonp"
    }).done(function (count) {
      var suffix = count === 1 ? "User" : "Users";
      $item.html(count + " " + suffix);
    });
  });
});
