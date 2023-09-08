$(document).ready(function () {
    $(".sign-out-btn").click(function () {
        $.ajax({
            url: "http://localhost:8000/api/core/user/logout/",
            type: "POST",
            contentType: "application/json",
            headers: { "X-CSRFToken": $.cookie("csrftoken"), 'Authorization': 'Bearer ' + $.cookie('token')},
            success: function (response) {
                $.removeCookie("token");
                window.location.reload();
            },
            error: function (error) {
                if (error.status === 404) {
                    $(".alert").append("<span>User not found</span>");
                    $(".alert").show();
                }
            },
        });
    });
});
