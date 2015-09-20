//            2.5MB - 2621440
//            5MB - 5242880
//            10MB - 10485760
//            20MB - 20971520
//            50MB - 5242880
//            100MB 104857600
//            250MB - 214958080
//            500MB - 429916160
function is_valid_file_size() {
    var file = $('#id_document')[0].files[0];
    return file.size <= 10485760;
}

function is_valid_file_extension() {
    var a = $('#id_document').val().split(".");
    if (a.length === 1 || ( a[0] === "" && a.length === 2 )) {
        return "";
    }
    var extension = a.pop().toLowerCase();

    valid_extensions = [
        'txt',
        'pdf',
        'doc',
        'docx',
        'ods',
        'jpeg',
        'png',
        'gif',
        'bmp',
        'xls',
        'xlsx',
        'csv',
        'xml',
        'html'
    ];

    return (valid_extensions.indexOf(extension) >= 0);
}


function is_valid_filename()  {
    var file = $('#id_document')[0].files[0];
    return file.name.length <= 40;
}


function is_valid_file()  {
    if (is_valid_file_size()) {

        if (is_valid_filename())  {
            return true;
        }
        else  {
            alert("Filename exceeds limit of 40 characters. Please rename the file and try again.");
            return false;
        }


    }
//        if (is_valid_file_extension()) {
//            return true;
//        }
//        else {
//            alert("Invalid file type. ");
//            return false;
//        }

    else {
        alert("File exceeds limit of 10MB");
        return false;
    }
}

function delete_file(delete_url, filename) {

    if (confirm("Are you sure you wish to delete " + filename + "?")) {
        window.location.href = delete_url;
    }
}

function upload_file(is_reviewer_document) {


    if (is_valid_file_size()) {

        if (is_valid_file_extension()) {
            ajax_upload_file(is_reviewer_document);
        }
        else {
            $('#documents_status_message').html("Invalid file format. Only .jpeg, .doc, .docx, .pdf, .txt and .ods are supported.");
            $('#documents_status').removeClass('hidden');
            $('#documents_status').toggleClass('bg-danger');
            $('#documents_status').toggleClass('bg-success');
        }
    }
    else {
        $('#documents_status_message').html("Maximum file size limit exceeded.");
        $('#documents_status').removeClass('hidden');
        $('#documents_status').toggleClass('bg-danger');
        $('#documents_status').toggleClass('bg-success');

    }
}


function save_application() {
    $('#action').val('SAVE');
    $('#grant_application_form').submit();
}

function submit_application() {
    if (confirm("You will not be able to edit the application once it has been submitted. Submit?")) {
        $('#action').val('SUBMIT');
        $('#grant_application_form').submit();
    }
}
//    AJAX FILE UPLOADS/DELETE/////////////////////////////////////////////////////////////////////////////////////////////////////////////
var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// functions to hide/show feedback whenever the application is saved



function get_field_label_by_field_name(name)  {
    var field_labels = {
        'grant_title': 'Grant Title',
        'grant_type': 'Grant Type',
        'grant_scheme':'Specific Scheme',
        'funds': 'Funds Applying For ($)',
        'school': 'School/Centre',
        'grant_id': 'Grant ID',
        'round':'Round'
    }
    return field_labels[name];
}


function feedback_success(field_name, value) {
    $('#form_group_' + field_name).removeClass('has-error');
    $('#form_group_' + field_name).addClass('has-success');
    $('#form_group_' + field_name).addClass('has-feedback');

    if (field_name == 'school')
        $('#id_' + field_name + ' option[value="' + value + '"]').prop('selected', true);
    else
        $('#id_' + field_name).val(value);

    $('#label_' + field_name).html(get_field_label_by_field_name(field_name) + ' - Saved')
    $('#label_' + field_name).removeClass('label-danger');
    $('#label_' + field_name).removeClass('label-primary');
    $('#label_' + field_name).addClass('label-success');
}

function feedback_fail(field_name) {
    $('#form_group_' + field_name).removeClass('has-success');
    $('#form_group_' + field_name).addClass('has-error');
    $('#label_' + field_name).html(get_field_label_by_field_name(field_name) + ' - Not Saved')
    $('#label_' + field_name).removeClass('label-success');
    $('#label_' + field_name).removeClass('label-primary');
    $('#label_' + field_name).addClass('label-danger');
}

function feedback_none(field_name) {
    $('#form_group_' + field_name).removeClass('has-success');
    $('#form_group_' + field_name).removeClass('has-error');
    $('#label_' + field_name).html(get_field_label_by_field_name(field_name))
    $('#label_' + field_name).removeClass('label-danger');
    $('#label_' + field_name).removeClass('label-success');
    $('#label_' + field_name).addClass('label-primary');

}


function display_save_feedback(field_name, feedback) {
    if (feedback == 'fail') {
        feedback_fail(field_name);
    }
    else {
        feedback_success(field_name, feedback);
    }
    setTimeout(
        function () {
            feedback_none(field_name)
        },
        1500
    );


}

function ajax_save_application() {
    $.ajax({
        url: $('#grant_application_form').attr('action'), // from application_edit.html template
        type: 'POST',
        data: $("#grant_application_form").serialize(),
        cache: false,
        beforeSend: function (xhr, settings) {

            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data, textStatus, jqXHR) {
            var obj = JSON.parse(data);
            var status = obj['status'];


            var funds = obj['funds'];
            var grant_title = obj['grant_title'];
            var grant_type = obj['grant_type'];
            var grant_scheme = obj['grant_scheme'];
            var school = obj['school'];
            var grant_id = obj['grant_id'];
            var round = obj['round'];

            if (school != null) {
                //display_save_feedback('school', school);
                location.reload();
            }
            if (funds != null) {
                display_save_feedback('funds', funds);
            }

            if (grant_title != null) {
                display_save_feedback('grant_title', grant_title);
            }

            if (grant_type != null) {
                //display_save_feedback('grant_type', grant_type);
                location.reload();

            }

            // grant_scheme is automatically wiped after changing grant_type. we don't want to display feedback in this case
            if (grant_scheme != null && grant_type == null) {
                display_save_feedback('grant_scheme', grant_scheme);
            }

            if (grant_id != null)  {
                display_save_feedback('grant_id', grant_id);
            }

            if (round != null){
                display_save_feedback('round',round);
            }

        },
        error: function (jqXHR, textStatus, errorThrown) {

        }
    });
}



function close_status_message(id) {
    $('#' + id).addClass('hidden');
}

function close_documents_message() {
    $('#documents_status').addClass('hidden');
}

function ajax_nominate_reviewer() {

    $.ajax({
        url: $('#reviewer_nomination_form').attr('action'), // from application_edit.html template
        type: 'POST',
        beforeSend: function (xhr, settings) {

            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            var obj = JSON.parse(data);


        },
        error: function (jqXHR, textStatus, errorThrown) {

        }
    });
}