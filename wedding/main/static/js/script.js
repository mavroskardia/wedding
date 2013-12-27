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
            $('.rsvp-messaging').empty().append('<p class="alert alert-danger">Could not complete action: ' + error + ' (' + status + ')</p>');
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
        $('.rsvp .email').attr('disabled', 'disabled');
        $('.rsvp .verify-container').replaceWith('<div class="col-lg-4 col-lg-offset-4 col-xs-12 form-group"><button class="submit-rsvp btn btn-primary btn-lg">RSVP!</button</div>');

        $('.rsvp-messaging').append('<p>Found email address "' + data.split(' ')[1] + '"!<br/>Please enter your name and those of your guests below:</p>');
        $('.rsvp .guests').append('<div class="form-group"><input type="text" class="form-control guestinput input-lg" placeholder="Name of first guest" name="guests[0]" /></div>');
        $('.rsvp .guests').append('<div class="form-group"><button class="addguest btn btn-default btn-lg">Add guest</button></div>');

        $('.rsvp .addguest:last').on('click', function (e) {
            e.preventDefault();
            var numGuests = $('.guestinput').length;
            $('.rsvp .guests .guestinput:last').parent().after('<div class="form-group"><input type="text" class="form-control guestinput input-lg" placeholder="Name of next guest" name="guests['+(numGuests)+']" /></div>');
        });

        $('.rsvp .submit-rsvp').on('click', function (e) {
            e.preventDefault();
            $(this).prop('disabled', true);
            $(this).after('<p class="post-rsvp-message">Submitting your RSVP...</p>');

            $.ajax({
                url: rsvp_submit_ajax_url,
                data: $('.rsvp').serialize(),
                type: 'post'
            })
            .done(postrsvp);
        });
    }

    function postrsvp(data) {
        console.log('post rsvp:');
        console.log(data);
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

