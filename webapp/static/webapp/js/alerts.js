/**
 * Fullscreen alerts for the pheme
 * accounts linking notification
 */
function cookie_exists(cookie_name) {
    return ((typeof $.cookie(cookie_name)) !== 'undefined')
}
function create_or_increment_cookie_counter(cookie_name) {
    if (cookie_exists(cookie_name))
    // If the cookie is set, then increase the cookie's counter
        $.cookie(cookie_name, parseInt($.cookie(cookie_name)) + 1, {path: '/'});
    else
    // Otherwise if it's not set, then set the counter to 1
        $.cookie(cookie_name, 1, {path: '/'});

}
function hide_box(dom_obj) {
    alert_box = $(dom_obj);
    alert_box.removeClass("dimmer");
    alert_box.hide();
}

function no_pheme_account(dom_obj, cookie_name)  {
    alert_box = $(dom_obj);
    alert_box.removeClass("dimmer");
    alert_box.hide();
    $.cookie(cookie_name, parseInt($.cookie(cookie_name)) + 10, {path: '/'});

}

function reset_count(cookie_name) {
    $.cookie(cookie_name, 1, {path: '/'});
}

pheme_cookie = "pheme_linked_004";
pheme_alertbox = "#alert_link";

$(document).ready(function () {

    // Display the hidden alert boxes
    $(pheme_alertbox).removeClass("hidden");

    if (cookie_exists(pheme_cookie) && $.cookie(pheme_cookie) > 2)
        hide_box(pheme_alertbox);
});