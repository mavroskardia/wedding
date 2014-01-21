import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from rsvp.models import Guest

# Create your views here.
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
                ret = HttpResponse('This email address was not in the guest list. Please check with Andy or Sarah.', status=500)
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

            guestlist = ['%s %s' % (guest.firstname,guest.lastname),]
            others = []

            for name in req.POST:
                if name.startswith('guests') and req.POST[name].strip():
                    others.append(req.POST[name].strip())

            guestlist = guestlist + others

            guest.total = len(guestlist)
            guest.additional = '|'.join(others)

            guest.save()

            ret['response'] = 'yes'
            ret['guests'] = '|'.join(guestlist)

        return HttpResponse(json.dumps(ret), content_type='application/json')