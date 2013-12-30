var RSVPVerifier = (function () {

    function verify(e) {
        e.preventDefault();

        $('.rsvp-messaging').append('<p>Checking your email</p>');

        var intervalId = window.setInterval(function () {
            var t = $('.rsvp-messaging').text();
            $('.rsvp-messaging').text(t + '.');
        }, 500);

        $.ajax({
            url: rsvp_ajax_url,
            data: $('form.rsvp').serialize(),
            type: 'post'
        })
        .done(postverify)
        .fail(function (xhr, error, status) {
            $('.rsvp-messaging').empty().append('<p class="alert alert-danger">Could not verify your email: ' + error + ' (' + status + ')</p>');
        })
        .always(function () {
            window.clearInterval(intervalId);
        });
    };

    function postverify(data) {
        $('.rsvp-messaging').empty();

        if (data.indexOf("success") != -1) {
            buildguestform(data);
        } else {
            $('.rsvp-messaging').append('<p class="alert alert-danger">Could not find your email address, please try again.</p>');
        }
    };

    function buildguestform(data) {
        var splits = data.split(' ');
        var name = splits[1];
        var email = splits[2];

        $('.rsvp .email').replaceWith('<input type="hidden" name="rsvp_email" value="' + email + '" />');
        $('.rsvp .verify-container').replaceWith('<div class="form-group"><button class="col-lg-2 col-lg-offset-5 col-xs-4 col-xs-offset-4 submit-rsvp btn btn-primary btn-lg">RSVP!</button</div>');

        $('.rsvp-messaging').append('<p>Thanks for RSVPing, ' + name + '!<br/><small>(' + email + ')</small><br/>Please enter the name of your guests below:</p>');
        $('.rsvp .guests').append('<div class="form-group"><input type="text" class="form-control guestinput input-lg" name="guests[0]" disabled value="'+name+'" /></div>');
        $('.rsvp .guests').append('<div class="form-group"><input type="text" class="form-control guestinput input-lg" placeholder="Name of first guest" name="guests[1]" /></div>');
        $('.rsvp .guests').append('<div class="form-group"><button class="addguest btn btn-default"><b>&plus;</b> Add Guest</button></div>');

        $('.rsvp .addguest:last').on('click', function (e) {
            e.preventDefault();
            var numGuests = $('.guestinput').length;
            $('.rsvp .guests .guestinput:last').parent().after('<div class="form-group"><input type="text" class="form-control guestinput input-lg" placeholder="Name of next guest" name="guests['+(numGuests)+']" /></div>');
        });

        $('.rsvp .submit-rsvp').on('click', function (e) {
            e.preventDefault();
            $(this).prop('disabled', true);
            $(this).after('<p class="clearfix col-lg-12 col-xs-12 post-rsvp-message">Submitting your RSVP...</p>');

            $.ajax({
                url: rsvp_submit_ajax_url,
                data: $('.rsvp').serialize(),
                type: 'post'
            })
            .done(postrsvp)
            .fail(rsvperror);
        });
    }

    function rsvperror(xhr, error, status) {
        $('.rsvp-messaging').empty().append('<p class="alert alert-danger">Could not RSVP: ' + error + ' (' + status + '). You should let Andy know.</p>');
    }

    function postrsvp(data) {
        var guestlist = data.split('|');
        var guestliststr = guestlist.join(', ');

        $('.rsvp').fadeOut(function () {
            $(this).replaceWith('<p class="rsvp-success">Successfully RSVP\'d with '+guestlist.length+' guest(s): ' + guestliststr + '</p>');
            $('a[href="#rsvp"]').click();
        });

        $('.rsvp-messaging').fadeOut(function () { $(this).remove(); });
    }

    return { verify: verify };

}());

$(document).ready(function () {

    $('a:not(.navbar a)').on('click', function (e) {
        var elt = $($(e.currentTarget).attr('href'));
        var top = elt.offset().top || 0;
        $('html,body').animate({ scrollTop: top }, 800, "swing");
    });

    $('.nav .navbar-collapse a').on('click', function () {
        $('.nav .navbar-toggle').click();
    });

    $('.verify').on('click', RSVPVerifier.verify);

});

