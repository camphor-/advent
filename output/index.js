$(document).ready(function () {
  "use strict";

  function getUrlWithoutProtocol(url) {
    return url.replace(/^https?:\/\//, "");
  }

  function matchDomain(url, domain){
    const u = new URL(url);
    return u.host.endsWith(domain);
  }

  const urlTo$ = {};
  $(".hateb-link")
    .each(function (i, item) {
      var $item = $(item);
      var url = getUrlWithoutProtocol($item.data("url"));
      if (url === "#" || url === "") { return; }
      urlTo$[url] = $item;
    });

  const urls = Object.keys(urlTo$);
  const PER_PAGE = 50 / 2;  // Every request contains both HTTP and HTTPS urls

  const notAddingCountDomains = ["hateblo.jp"]

  for (let page = 0; page < Math.ceil(urls.length / PER_PAGE); page++) {
    const urlsWithoutProtocol = [];
    urls
      .slice(page * PER_PAGE, (page + 1) * PER_PAGE)
      .forEach(function (url) {
        urlsWithoutProtocol.push("http://" + url);
        urlsWithoutProtocol.push("https://" + url);
      });

    // Ref: http://developer.hatena.ne.jp/ja/documents/bookmark/apis/getcount
    const query = urlsWithoutProtocol
      .map(function (link) { return "url=" + encodeURIComponent(link); })
      .join("&");
    $.ajax({
      url: "https://bookmark.hatenaapis.com/count/entries?" + query,
      dataType: "jsonp"
    }).done(function (counts) {
      Object.entries(counts).forEach(function (urlCount) {
        const url = urlCount[0];
        const urlWithoutProtocol = getUrlWithoutProtocol(url);
        const $item = urlTo$[urlWithoutProtocol];
        const previousCount = $item.data("count") ? $item.data("count") : 0 ;

        let count = urlCount[1];
        const isMatched = notAddingCountDomains.some(function (domain){
          return matchDomain($item.data("url"), domain)
        });
        if (!isMatched) {
          count += previousCount;
        }

        const suffix = count === 1 ? "User" : "Users";
        $item.data("count", count);
        $item.html(count + " " + suffix);
      });
    });
  }
});
