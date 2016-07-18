$(function () {
    $("#comments-form").submit(function() {
        $("#comments-form input[type=submit]").attr("disabled", "disabled");
    });

    var pixelRatio = window.devicePixelRatio || 1;
    var deviceHeight = $(window).height() * pixelRatio;
    var iOS = /iPad|iPhone|iPod/.test(navigator.platform);
    if (iOS) {
        deviceHeight = screen.availHeight + 30;
    }

    if ($(window).width() > 840 * pixelRatio) {
        $(".full-height").css("height",  deviceHeight + "px");
    }
    $(".full-height-forced").css("height", deviceHeight + "px");
});

$(window).load(function() {
    $(".block-timeline").each(function (i) {
        make_timeline($(this).find(".block-timeline__block"));
    });
});

function nick(nick) {
    $('#comment-text').val($('#comment-text').val() + "<b>" + nick + "</b>, ").focus();
}

function make_timeline($blocks) {
    var swap_next = false;
    $blocks.each(function (i) {
        console.debug("BLOCK", $(this), $(this).position());
        if (swap_next) {
            // надо поменять местами
            if ($(this).hasClass("left")) {
                $(this).removeClass("left").addClass("right");
            } else {
                $(this).removeClass("right").addClass("left");
            }
        }

        // если левый оказался справа
        if ($(this).hasClass("left") && $(this).position().left > 50) {
            $(this).removeClass("left").addClass("right");
            swap_next = !swap_next;
        }

        // если правый оказался слева
        if ($(this).hasClass("right") && $(this).position().left < 300) {
            $(this).removeClass("right").addClass("left");
            swap_next = !swap_next;
        }
    });
}