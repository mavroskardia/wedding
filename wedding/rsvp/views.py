import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from rsvp.models import Guest


def rsvp_ajax(req):

    email = 'boo'
    ret = HttpResponse('Unknown failure.', status=500)

    if req.method == 'POST':
        email = req.POST['email']
        if '@' not in email:
            ret = HttpResponse('Invalid email address, please try again.', status=500)
        else:
            try:
                guest = Guest.objects.get(email=email)
                ret = HttpResponse('success {guest.firstname} {guest.lastname} {guest.email}'.format(guest=guest))
            except Guest.DoesNotExist as e:
                guest = Guest(email=email, rsvpd=False, saidyes=False, coming_to_welcome=False)
                guest.save()
                ret = HttpResponse('success <new> Last {guest.email}'.format(guest=guest))
            except Exception as e:
                ret = HttpResponse('An unknown error occurred: %s' % e)

    return HttpResponse(ret)

class RsvpSubmitAjax(View):

    def post(self, req):
        ret = {}

        guest = get_object_or_404(Guest, email=req.POST['rsvp_email'])
        guest.rsvpd = True

        if 'notattending' in req.POST:
            ret['response'] = 'no'
            guest.saidyes = False
        else:
            guest.saidyes = True
            
            if 'guests[0]' in req.POST:
                namepieces = req.POST['guests[0]'].split(' ')
                guest.firstname, guest.lastname = namepieces[0], namepieces[1]
            
            guestlist = ['%s %s' % (guest.firstname,guest.lastname),]
            others = []

            for name in req.POST:
                if name.startswith('guests') and not name.endswith('[0]') and req.POST[name].strip():
                    others.append(req.POST[name].strip())

            guestlist = guestlist + others

            guest.total = len(guestlist)
            guest.additional = '|'.join(others)
            guest.song = req.POST.get('song_request', 'no request')
            guest.comments = req.POST.get('comments', 'no comments')
            guest.coming_to_welcome = req.POST.get('coming_saturday', False)

            guest.save()

            ret['response'] = 'yes'
            ret['guests'] = '|'.join(guestlist)

        return HttpResponse(json.dumps(ret), content_type='application/json')