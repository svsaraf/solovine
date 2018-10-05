from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from friends.models import Contact
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login')
def profile(request, email):
    context = {}
    users = User.objects.filter(email=email)
    if len(users) != 1:
        return HttpResponseRedirect('/posts')
    vieweduser = users[0]
    context['contacts'] = Contact.objects.filter(accepted=True, sender=vieweduser)
    if vieweduser == request.user:
        context['sent_requests'] = Contact.objects.filter(accepted=False, sender=vieweduser)
        context['received_requests'] = Contact.objects.filter(accepted=False, receiver=vieweduser)
        context['me'] = True
    elif vieweduser != request.user:
        if len(Contact.objects.filter(accepted=True, sender=vieweduser, receiver=request.user)) < 1: #not a friend
            if len(Contact.objects.filter(accepted=False, sender=vieweduser, receiver=request.user)) < 1: #potential friend has sent a request
                if len(Contact.objects.filter(accepted=False, sender=request.user, receiver=vieweduser)) < 1: #you have already sent a request
                    context['can_send_request'] = True
                    context['me'] = False
    context['profile'] = users[0]

    return render(request, 'friends/profile.html', context)

@login_required(login_url='/login')
def send(request, email):
    context = {}
    if request.method == 'POST':
        u = User.objects.get(email=email)
        c = Contact(sender=request.user, receiver=u, accepted=False)
        c.save()
        context['message'] = 'Sent!'
        return render(request, 'friends/message.html', context)
    return render(request, 'friends/profile.html', context)

@login_required(login_url='/login')
def cancel(request, email):
    context = {}
    if request.method == 'POST':
        u = User.objects.get(email=email)
        c = Contact.objects.filter(sender=request.user, receiver=u, accepted=False)[0]
        c.delete()
        context['message'] = 'Cancelled!'
        return render(request, 'friends/message.html', context)
    return render(request, 'friends/profile.html', context)

@login_required(login_url='/login')
def accept(request, email):
    context = {}
    if request.method == 'POST':
        u = User.objects.get(email=email)
        c = Contact.objects.get(sender=u, receiver=request.user, accepted=False)
        c.accepted = True
        c_compliment = Contact(sender=request.user, receiver=u, accepted=True)
        c.save()
        c_compliment.save()
        context['message'] = 'Request accepted.'
        return render(request, 'friends/message.html', context)
    return render(request, 'friends/profile.html', context)


@login_required(login_url='/login')
def reject(request, email):
    context = {}
    if request.method == 'POST':
        u = User.objects.get(email=email)
        c = Contact.objects.get(sender=u, receiver=request.user, accepted=False)
        c.delete()
        context['message'] = 'Rejected!'
        return render(request, 'friends/message.html', context)
    return render(request, 'friends/profile.html', context)
