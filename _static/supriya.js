$(document).ready(function() {
  $("div.container.inherited dl.py").each(function() {
    $(this).addClass("closed");
    var dl = $(this);
    var dt = $(this).children("dt");
    var dd = $(this).children("dd");
    if (dd.html()) {
      var toggle = dt.prepend('<span class="toggle"></span>').click(function() {
        $(dl).toggleClass("open");
        $(dl).toggleClass("closed");
      });
    }
  });
});
