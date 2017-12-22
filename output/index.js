$(document).ready(function () {
  "use strict";
  var $table = $("table.schedule");

  var urlTo$ = {};
  $(".hateb-link")
    .each(function (i, item) {
      var $item = $(item);
      var url = $item.data("url");
      if (url === "#" || url === "") { return; }
      urlTo$[url] = $item;
    });

  var urls = Object.keys(urlTo$);
  var PER_PAGE = 50;

  for (var page = 0; page < Math.ceil(urls.length / PER_PAGE); page++) {
    var query = urls
      .slice(page * PER_PAGE, (page + 1) * PER_PAGE)
      .map(function(link) { return "url=" + encodeURIComponent(link); })
      .join("&");
    $.ajax({
      url: "https://b.hatena.ne.jp/entry.counts?" + query,
      dataType: "jsonp"
    }).done(function (counts) {
      Object.entries(counts).forEach(function(urlCount) {
        var url = urlCount[0];
        var count = urlCount[1];
        var $item = urlTo$[url];
        var suffix = count === 1 ? "User" : "Users";
        $item.html(count + " " + suffix);
      });
    });
  }
});
