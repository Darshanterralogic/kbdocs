$(document).ready(function () {
    $(".edit-kbdoc-form").submit(function () {
        let data = {};
        let kbdocId = $("#kbdoc_id").val();
        $.each($('.edit-kbdoc-form').serializeArray(), function(i, field) {
            data[field.name] = field.value;
        });
        setTimeout(function () {
            $.ajax({
                url: "http://localhost:8000/api/core/kbdocs/" + kbdocId + "/",
                type: "PUT",
                contentType: "application/json",
                data: JSON.stringify(data),
                headers: { "X-CSRFToken": $.cookie("csrftoken"), 'Authorization': 'Bearer ' + $.cookie('token')},
                success: function (response) {
                    if (response.success) {
                        window.location.reload();
                    }
                },
                error: function (error) {
                    console.log(error)
                },
            });
        }, 500);
        return false;
    });

    $(".add-kbdoc-form").submit(function () {
        let data = {};
        $.each($('.add-kbdoc-form').serializeArray(), function(i, field) {
            data[field.name] = field.value;
        });
        setTimeout(function () {
            $.ajax({
                url: "http://localhost:8000/api/core/kbdocs/",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(data),
                headers: { "X-CSRFToken": $.cookie("csrftoken"), 'Authorization': 'Bearer ' + $.cookie('token')},
                success: function (response) {
                    if (response.success) {
                        window.location.href = '/viewkbdocs/';
                    }
                },
                error: function (error) {
                    console.log(error)
                },
            });
        }, 500);
        return false;
    });
});