/**
 * Created by wangkai on 2017/12/14.
 */
;

// {{ super() }}

$(function(){
    $("#up").on("mousedown touchstart", function (e) {
        $.get("carEvents/go-true");
        // e.preventDefault();

    });
    $("#up").on("mouseup touchend touchcancel", function (e) {
          $.get("carEvents/go-false");
          $(this).blur();
         e.preventDefault();
    });

    $("#down").on("mousedown touchstart", function () {
        $.get("carEvents/down-true");
    });
     $("#down").on("mouseup touchend touchcancel", function () {
        $.get("carEvents/down-false");
    });

     $("#left").on("mousedown touchstart", function () {
        $.get("carEvents/left-true");
    });
     $("#left").on("mouseup touchend touchcancel", function () {
       $.get("carEvents/left-false");
    });

    $("#right").on("mousedown touchstart", function () {
        $.get("carEvents/right-true");
    });
     $("#right").on("mouseup touchend touchcancel", function () {
       $.get("carEvents/right-false");
    });

    $("#stop").on("click touchend tap", function () {
         $.get("carEvents/stop-true");
    });

});

window.onload = function () {
        document.oncontextmenu = function(){
        event.returnValue = false;
    };
    document.body.addEventListener('touchstart', function () { });
    window.ontouchstart = function(e) {
    e.preventDefault();
};
}
