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
        var firstname = splits[1];
        var lastname = splits[2];
        var email = splits[3];

        $('.rsvp .email').parent().replaceWith('<input type="hidden" name="rsvp_email" value="' + email + '" />');

        var msg = '<p>Thank you';

        if (firstname != '<new>') {
            msg += ', ' + firstname;
        }

        $('.rsvp-messaging').append(msg + '\
            <small>(' + email + ')</small><br/>\
            <strong>Before we can process your RSVP</strong>, please indicate if you will be able to attend, your name, and the names of your guests below:</p>');

        $('.rsvp .verify-container').replaceWith('<div class="clear col-lg-4 col-lg-offset-4"> \
                <hr />\
                <div class="clearfix">\
                    <div class="form-group text-left">\
                        <input id="attending-yes" type="radio" name="attending" value="true" />\
                        <label for="attending-yes" class="smaller">Attending</label>\
                        <div class="col-lg-offset-1 col-xs-offset-1">\
                            <input id="coming-saturday" type="checkbox" name="coming_saturday" value="true" />\
                            <label for="coming-saturday" class="smaller">Saturday Dinner, too!</label>\
                        </div>\
                    </div>\
                </div>\
                <div class="clearfix">\
                    <div class="form-group text-left">\
                        <input id="attending-no" type="radio" name="attending" value="false" />\
                        <label for="attending-no" class="smaller">Unable to attend</label>\
                    </div>\
                </div>\
            </div>\
            <div class="clear col-lg-4 col-lg-offset-4">\
                <hr />\
                <div class="form-group text-left">\
                    <label class="smaller" for="song-request">I will dance if you play...</label>\
                    <textarea id="song-request" name="song_request" class="form-control" placeholder="Song request!" />\
                </div>\
                <div class="form-group text-left">\
                    <label class="smaller" for="comments">Comments?</label>\
                    <textarea id="comments" name="comments" class="form-control" placeholder="Any comments are appreciated!" />\
                </div>\
                <div class="form-group">\
                    <button class="col-lg-3 col-lg-offset-4 col-xs-4 col-xs-offset-4 submit-rsvp btn btn-primary btn-lg">RSVP!</button>\
                </div>\
            </div>');

        var guestlisthtml = '<div class="form-group col-lg-4 col-lg-offset-4">\
            <input type="text" class="form-control guestinput input-lg" name="guests[0]"';

        if (firstname == '<new>') {
            guestlisthtml += ' placeholder="Enter your name here"';
        } else {
            guestlisthtml += ' disabled value="' + (firstname + ' ' + lastname) + '" ';
        }

        guestlisthtml += ' />\
            </div>';

        $('.rsvp .guests')
            .append(guestlisthtml)
            .append('<div class="form-group col-lg-4 col-lg-offset-4">\
            <input type="text" class="form-control guestinput input-lg" placeholder="Additional guest\'s name" name="guests[1]" />\
            </div>')
            .append('<div class="form-group col-lg-4 col-lg-offset-4">\
            <button class="addguest btn btn-default"><b>&plus;</b> Add Guest</button>\
            </div>');

        $('.rsvp .addguest:last').on('click', function (e) {
            e.preventDefault();
            var numGuests = $('.guestinput').length;
            $('.rsvp .guests .guestinput:last').parent().after('<div class="form-group col-lg-4 col-lg-offset-4"><input type="text" class="form-control guestinput input-lg" placeholder="Name of next guest" name="guests['+(numGuests)+']" /></div>');
        });

        $('.rsvp .submit-rsvp').on('click', function (e) {
            e.preventDefault();
            e.stopImmediatePropagation();

            $(this).replaceWith('<p class="clearfix col-lg-12 col-xs-12 post-rsvp-message">Submitting your RSVP...</p>');

            $.ajax({
                url: rsvp_submit_ajax_url,
                data: $('.rsvp').serialize(),
                dataType: 'json',
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
        var message = 'Thank you for your response.<br/>';

        if (data.response == 'no') {
            message += ' We are sorry you cannot attend.';
        } else {
            var guestlist = data.guests.split('|');
            var guestliststr = guestlist.join(', ');
            guestliststr = guestliststr.replace(/^(.*),(.*)$/, '$1 and $2');
            if (guestlist.length > 1) {
                message += ' You and your guests make ' + guestlist.length + ': ' + guestliststr;
            } else {
                message += ' We can\'t wait for you to join us!';
            }
        }

        $('.rsvp').fadeOut(function () {
            $(this).replaceWith('<p class="rsvp-success">' + message + '</p>');
            var elt = $('#rsvp');
            var top = elt.offset().top || 0;
            $('html,body').animate({ scrollTop: top }, 800, "swing");
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
        $('.navbar-collapse').collapse('hide');
    });

    $('.nav .navbar-collapse a').on('click', function () {
        $('.navbar-collapse').collapse('hide');
    });

    $('.verify').on('click', function (e) {
        RSVPVerifier.verify(e);
        $('.fg').fadeOut('fast');
    });

    $('img').lazyload({
        event: 'myimgload',
        effect: 'fadeIn'
    });

    setTimeout(function () {
        $('img').trigger('myimgload');
    }, 500);

});

var CountUp = (function () {
    function CountUp() {
        var self = this;
    }
    
    CountUp.prototype.init = function () {
        var startDate = new Date('2014/08/31 16:58');

        window.setInterval(function () {
            var msLeft = new Date() - startDate;
            var e = document.getElementById('countdown');

            var weeks = (msLeft / 604800000) | 0;
            msLeft -= weeks * 604800000;

            var days = (msLeft / 86400000) | 0;
            msLeft -= days * 86400000;

            var hours = (msLeft / 3600000) | 0;
            msLeft -= hours * 3600000;

            var minutes = (msLeft / 60000) | 0;
            msLeft -= minutes * 60000;

            var seconds = (msLeft / 1000) | 0;
            msLeft -= seconds * 1000;

            e.innerHTML = (weeks + ' weeks, ' + days + ' days, ' + hours + ' hours, ' + minutes + ' minutes, and ' + seconds + ' seconds');
        }, 1000);
    };
    
    return CountUp;
}());