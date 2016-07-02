from django.conf import settings
from django.shortcuts import redirect, render
from django.core.mail import send_mail

# Create your views here.
from .forms import contactForm


def landingpage_view(request):
    return render(request, 'landingpage/landingpage.html')


def impressum(request):
    ''' send Email to grandmas-beautytips@gmx.de
        send via Impressum'''
    contact_form = contactForm(request.POST or None)
    if contact_form.is_valid():
        form_email = contact_form.cleaned_data.get('email')
        form_first_name = contact_form.cleaned_data.get('name')
        # form_surname = form.cleaned_data.get('surname')
        form_message = contact_form.cleaned_data.get('nachricht')

        subject = 'Anfrage von Grandmas-Beautytips'
        contact_message = "From: {} \n\n" \
                            " Message: {}\n\n" \
                            "via: {}".format(form_first_name, form_message, form_email)
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email]
        send_mail(
                subject,
                contact_message,
                from_email,
                to_email,
                fail_silently=False
        )
        return redirect('landingpage:send')

    context = {
        'contact_form' : contact_form,
    }
    return render(request, 'impressum/impressum.html', context)

def send(request):
    return render(request, 'form_send.html')
