$(document).ready(function () {
  "use strict";
  var $table = $("table.schedule");

  function getUrlWithoutProtocol(url) {
    return url.replace(/^https?:\/\//, "");
  }

  var urlTo$ = {};
  $(".hateb-link")
    .each(function (i, item) {
      var $item = $(item);
      var url = getUrlWithoutProtocol($item.data("url"));
      if (url === "#" || url === "") { return; }
      urlTo$[url] = $item;
    });

  var urls = Object.keys(urlTo$);
  var PER_PAGE = 50 / 2;  // Every request contains both HTTP and HTTPS urls

  for (var page = 0; page < Math.ceil(urls.length / PER_PAGE); page++) {
    var urlsWithoutProtocol = [];
    urls
      .slice(page * PER_PAGE, (page + 1) * PER_PAGE)
      .forEach(function (url) {
        urlsWithoutProtocol.push("http://" + url);
        urlsWithoutProtocol.push("https://" + url);
      });

    var query = urlsWithoutProtocol
      .map(function(link) { return "url=" + encodeURIComponent(link); })
      .join("&");
    $.ajax({
      url: "https://b.hatena.ne.jp/entry.counts?" + query,
      dataType: "jsonp"
    }).done(function (counts) {
      Object.entries(counts).forEach(function(urlCount) {
        var url = urlCount[0];
        var urlWithoutProtocol = getUrlWithoutProtocol(url);
        var $item = urlTo$[urlWithoutProtocol];
        var previousCount = $item.data("count");
        previousCount = previousCount ? previousCount : 0;
        var count = urlCount[1] + previousCount;
        var suffix = count === 1 ? "User" : "Users";
        $item.data("count", count);
        $item.html(count + " " + suffix);
      });
    });
  }
});
