$(document).ready(function () {
    $(".signup-form").submit(function () {
        let email = $("#employeeEmail").val();
        let employeeId = $("#employeeId").val();
        let password = $("#employeePassword").val();
        let verifyPassword = $("#verifyPassword").val();
        let firstName = $("#firstName").val();
        let lastName = $("#lastName").val();
        let passwordUpperCaseRegex = new RegExp("[A-Z]");
        let passwordSpecialCharRegex = /[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
        let passwordDigitRegex = new RegExp("[0-9]");
        let hasError = false;
        let errorClasses = [];
        $('[class^="invalid-"]').hide();
        $('[class^="empty-"]').hide();
        $(".alert").find('span').remove();
        $(".alert").hide();

        if (firstName === "") {
            hasError = true;
            errorClasses.push('empty-first-name');
        }
        if (lastName === "") {
            hasError = true;
            errorClasses.push('empty-last-name');
        }
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
        if (verifyPassword === "") {
            hasError = true;
            errorClasses.push('empty-verify-password');
        } else if (password !== verifyPassword) {
            hasError = true;
            errorClasses.push('invalid-verify-password');
        }
        if (hasError && errorClasses) {
            $.each(errorClasses, function (i, errorClass) {
                $("." + errorClass).show();
            });
            return false;
        }

        $.ajax({
            url: window.location.origin + "/api/core/user/create/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ email: email, emp_id: employeeId, password: password, first_name: firstName, last_name: lastName }),
            success: function (response) {
                if (response.success) {
                    window.location.href = "/";
                } else {
                    $(".alert").append("<span>" + response.error + "</span>");
                    $(".alert").show();
                }
            },
            error: function (error) {
              console.error("ERROR WHILE LOGGING IN ->", error);
            },
        });
        // console.log("SUBMITED");
        return false;
    });
});