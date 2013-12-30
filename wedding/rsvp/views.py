from django.http import HttpResponse

from django.shortcuts import render

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
                ret = HttpResponse('success %s %s' % (guest.name, guest.email))
            except Guest.DoesNotExist as e:
                ret = HttpResponse('This email address was not in the guest list. Please check with Andy or Sarah.', status=500)

    return HttpResponse(ret)

def rsvp_submit_ajax(req):

    if req.method != 'POST':
        return HttpResponse('failure')

    guest = Guest.objects.get(email=req.POST['rsvp_email'])

    guestlist = [guest.name,]

    for name in req.POST:
        if name.startswith('guests') and req.POST[name].strip():
            guestlist.append(req.POST[name].strip())

    return HttpResponse('|'.join(guestlist))