$(document).ready(function () {
    $(".login-form").submit(function () {
        let email = $("#employeeEmail").val();
        let employeeId = $("#employeeId").val();
        let password = $("#employeePassword").val();
        let passwordUpperCaseRegex = new RegExp("[A-Z]");
        let passwordSpecialCharRegex = /[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
        let passwordDigitRegex = new RegExp("[0-9]");
        let hasError = false;
        let errorClasses = [];
        $('[class^="invalid-"]').hide();
        $('[class^="empty-"]').hide();
        $(".alert").find('span').remove();
        $(".alert").hide();
            
        if (email === "") {
            hasError = true;
            errorClasses.push('invalid-email-id');
        }
        if (employeeId === "") {
            hasError = true;
            errorClasses.push('empty-employee-id');
        } else if (!(/^PSI-\d{4}$/.test(employeeId))) {
            hasError = true;
            errorClasses.push('invalid-employee-id');
        }
        if (password === "") {
            hasError = true;
            errorClasses.push('empty-password');
        } else if (!(passwordUpperCaseRegex.test(password)) || !(passwordDigitRegex.test(password)) || !(passwordSpecialCharRegex.test(password))) {
            hasError = true;
            errorClasses.push('invalid-password');
        }
        if (hasError && errorClasses) {
            $.each(errorClasses, function (i, errorClass) {
                $("." + errorClass).show();
            });
            return false;
        }

        $.ajax({
            url: "http://localhost:8000/api/core/user/login/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ email: email, emp_id: employeeId, password: password }),
            success: function (response) {
                if (response.success) {
                    $.cookie("token", response.tokens.access);
                    window.location.reload();
                } else {
                    $(".alert").append("<span>" + response.error + "</span>");
                    $(".alert").show();
                }
            },
            error: function (error) {
                if (error.status === 404) {
                    $(".alert").append("<span>User not found</span>");
                    $(".alert").show();
                }
            },
        });
        return false;
    });
});