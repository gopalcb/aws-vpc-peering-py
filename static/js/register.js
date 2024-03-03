/**
 * app.js
 * handle signin page async ops
 * Author: Gopal Chandra Bala
*/

/** SCOPE **/
let page = $('.register-block')
var auth_token = ''
var user_obj = {}

/** FUNCTIONS BLOCK **/
function get_register_creds() {
    let creds_obj = {
        'username': $('.username').val().trim(),
        'password': $('.password').val(),
        'confirm_password': $('.confirm-password').val()
    }

    console.log(creds_obj)
    return creds_obj
}

function handle_form_error(err_msg, element) {
    if (err_msg == '') {
        element.css('border', '1px solid #57557A')
        element.removeClass('vf').removeClass('vs').removeClass('vs')
        element.parent().find('.err').text('')
        element.parent().find('.err').hide()
    }
    else {
        element.css('border', '1px solid red')
        element.removeClass('vf').removeClass('vs').removeClass('vf')
        element.parent().find('.err').text(err_msg)
        element.parent().find('.err').show()
    }
}

function validate_username_password(element) {
    let creds_obj = get_register_creds()

    if (element.hasClass('username')) {
        let err = ''
        // username length should be > 3
        if (creds_obj['username'].length <= 3) {
            err = 'Invalid username. Length should be greater than 3 characters long.'
        }

        if (err != '') {
            handle_form_error(err, $('.username'))
            return false
        }
        else {
            handle_form_error('', $('.username'))
            return true
        }
    }

    if (element.hasClass('password')) {
        let err = ''
        // username length should be > 5
        if (creds_obj['password'].length <= 5) {
            err = 'Invalid password. Length should be greater than 5 characters long.'
        }

        if (err != '') {
            handle_form_error(err, $('.password'))
            return false
        }
        else {
            handle_form_error('', $('.password'))
            return true
        }
    }

    return true
}

function check_username_availability() {
    let creds_obj = get_register_creds()
    let valid = validate_username_password($('.username'))
    if (valid) {
        $.ajax('/check_username_availability', {
            type: 'POST',  // http method
            data: creds_obj,  // data to submit
            contentType: "application/json",
            success: function (data, status, xhr) { // success callback
                let status_ = data.status
                console.log('username availability status: ' + status_)
                if (status_) {
                    handle_form_error('', $('.username'))
                }
                else {
                    handle_form_error('Username is not available', $('.username'))
                }
            },
            error: function (jqXhr, textStatus, errorMessage) { // error callback
                
            }
        });
    }
}


function clear_form() {
    $('.username').val('')
    $('.password').val('')
    $('.confirm-password').val('')
}


function register() {
    let creds_obj = get_register_creds()

    $.ajax('/user_signup', {
        type: 'POST',  // http method
        data: creds_obj,  // data to submit
        contentType: "application/json",
        success: function (data, status, xhr) { // success callback
            let status_ = data.status
            console.log('signin status: ' + status_)
            if (status_) {
                alert('Registration complete!')
                clear_form()
            }
            else {
                alert('Registration failed!')
                // clear_form()
            }
        },
        error: function (jqXhr, textStatus, errorMessage) { // error callback
            alert('Registration failed!')
            // clear_form()
        }
    });

}


/** BUTTON CLICK EVENTS BLOCK **/
$('.btn-register').click(function() {
    if (page.find('.vf').length > 0) {
        // has validation error
        page.find('.vf')[0].focus()
    }
    else {
        register()
    }
})


$('.confirm-password').change(function() {
    let pass1 = $('.password').val()
    let pass2 = $('.confirm-password').val()
    if (pass1 != pass2) {
        handle_form_error('Entered a valid confirm password.', $('.confirm-password'))
    }
    else {
        handle_form_error('', $('.confirm-password'))
    }
})


$('.username, .password').change(function() {
    // check_username_availability()
    validate_username_password($(this))
})
