$(document).ready(function() {
    $("div.abjad-book-image-source").toggle();
    $("div.abjad-book-image > img").click(function(event) {
        $(this).parent().siblings("div.abjad-book-image-source").toggle(250);
    });
});