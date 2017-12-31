/**
 * Created by wangkai on 2017/12/14.
 */
;

// {{ super() }}

$(function () {

    var $box_up_down = $('.box_up_down');
    var box_up_down_pos = $box_up_down.offset();
    // var box_up_down_pos_w = $box_up_down.width();
    var box_up_down_pos_h = $box_up_down.height();
    var $box_up_down_parent = $('.box_up_down').parent();
    var box_up_down_parent_pos = $box_up_down_parent.offset();
    // var box_up_down_parent_pos_w = $box_up_down_parent.width();
    var box_up_down_parent_pos_h = $box_up_down_parent.height();
    $box_up_down.css({top: box_up_down_parent_pos_h / 2 - box_up_down_pos_h / 2});
    $box_up_down.draggable({
        containment: 'parent',  // 约束其只能在父级内拖动
        axis: 'y', // 只能在x轴
        opacity: 0.5,  // 拖动时透明度
        drag: function (ev, ui) {
            // console.log(ui);
            console.log(ui.position.top);
            // ev.preventDefault();
        }
    });
     $box_up_down.on("mouseup touchend touchcancel", function () {
        $box_up_down.css({top: box_up_down_parent_pos_h / 2 - box_up_down_pos_h / 2});
    });
    var $box_left_right = $('.box_left_right');
    var box_left_right_pos = $box_left_right.offset();
    var box_left_right_pos_w = $box_left_right.width();
    var box_left_right_pos_h = $box_left_right.height();
    var $box_left_right_parent = $('.box_left_right').parent();
    var box_left_right_parent_pos = $box_left_right_parent.offset();
    var box_left_right_parent_pos_w = $box_left_right_parent.width();
    var box_left_right_parent_pos_h = $box_left_right_parent.height();
    $box_left_right.css({left: box_left_right_parent_pos_w / 2 - box_left_right_pos_w / 2});
    $box_left_right.draggable({
        containment: 'parent',  // 约束其只能在父级内拖动
        axis: 'x', // 只能在x轴
        opacity: 0.5,  // 拖动时透明度
        drag: function (ev, ui) {
            // console.log(ui);
            console.log(ev);
            // ev.preventDefault();
            // ev.setDefaults();
            console.log(ui.position.left);
        }
    });
     $box_left_right.on("mouseup touchend touchcancel", function () {
        $box_left_right.css({left: box_left_right_parent_pos_w / 2 - box_left_right_pos_w / 2});
    });


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
    document.oncontextmenu = function () {
        event.returnValue = false;
    };
    document.body.addEventListener('touchstart', function () {
    });
    window.ontouchstart = function (e) {
        e.preventDefault();
    };
}
