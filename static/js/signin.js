/**
 * app.js
 * handle signin page async ops
 * Author: Gopal Chandra Bala
*/

/** SCOPE **/
let page = $('.signin-block')
var auth_token = ''
var user_obj = {}

/** FUNCTIONS BLOCK **/
function get_signin_creds() {
    let creds_obj = {
        'username': $('.username').val().trim(),
        'password': $('.password').val()
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
    let creds_obj = get_signin_creds()

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
    let creds_obj = get_signin_creds()
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
}


function signin() {
    let creds_obj = get_signin_creds()

    $.ajax('/user_signin', {
        type: 'POST',  // http method
        data: creds_obj,  // data to submit
        contentType: "application/json",
        success: function (data, status, xhr) { // success callback
            let status_ = data.status
            let token_ = data.token
            let user_ = data.user
            console.log('signin status: ' + status_)
            if (status_) {
                // alert('success')
                auth_token = token_
                user_obj = user_

                clear_form()
                dashboard()
            }
            else {
                alert('not success')
                clear_form()
                auth_token = ''
                user_obj = {}
            }
        },
        error: function (jqXhr, textStatus, errorMessage) { // error callback
            alert('not success')
            clear_form()
            auth_token = ''
            user_obj = {}
        }
    });

}


function dashboard() {
    let usr_data = user_obj
    $.ajax('/dashboard', {
        type: 'POST',  // http method
        data: usr_data,  // data to submit
        contentType: "application/json",
        headers: {"x-access-token": auth_token},
        success: function (data, status, xhr) { // success callback
            let status_ = data.status
            let uname = data.username
            
            if (status_) {
                alert('success : welcome - ' + uname)
            }
            else {
                alert('not success')
            }
        },
        error: function (jqXhr, textStatus, errorMessage) { // error callback
        }
    });
}


/** BUTTON CLICK EVENTS BLOCK **/
$('.btn-signin').click(function() {
    if (page.find('.vf').length > 0) {
        // has validation error
        page.find('.vf')[0].focus()
    }
    else {
        signin()
    }
})


$('.username, .password').change(function() {
    // check_username_availability()
    validate_username_password($(this))
})
