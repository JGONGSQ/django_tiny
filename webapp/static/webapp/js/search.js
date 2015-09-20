function get_url_vars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
        //vars[key] = value.replace("+"," ").replace("#","").replace("%2F","/");
        vars[key] = value.split("+").join(" ").split("#").join("").split("%2F").join("/");
    });
    return vars;
}

function toggle_search_bar() {
    $('#search_table').toggleClass("hidden");
    $('#hide_search_bar').toggleClass("hidden");
    $('#search_bar').toggleClass('hidden');
}

function clear_input() {
    $('#username').val('');
    $('#application').val('');
    $('#gid').val('');
    $('#date_start').val('');
    $('#date_end').val('');
    var application_page = get_url_vars()['application_page'];
    var order_value = get_url_vars()['order_by'];
    if (application_page != null) {
        $('#submit_page').val(application_page);
    }
    if (order_value != null) {
        //$('#submit_id').val(order_value);
        $('#order_by').val(order_value);
    }
}


function  order_applications() {
    var field = $('#select_order_by').val();
    var order = $('#select_order').val();
    $('#order_by').val(order + field);
    $('#search_form').submit();
}


function submitPage(v) {
    var order_value = get_url_vars()['order_by'];
    if (order_value != null) {
        //$('#submit_id').val(order_value);
        $('#order_by').val(order_value);
    }

    $('#submit_page').val(v);
    $('#search_form').submit();
}