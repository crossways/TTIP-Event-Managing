from django import forms

class contactForm(forms.Form):
    ''' send Email to grandmas-beautytips@gmx.de
        send via Impressum'''
    name = forms.CharField(max_length=25, required='True')
    # surname = forms.CharField(max_length=25, required='False')
    email = forms.EmailField()
    nachricht = forms.CharField(max_length=2000, widget=forms.Textarea)

    def clean_email(self):
        '''Evaluationsprozess für eingegebene Emails'''
        email = self.cleaned_data.get('email')      # bezieht email (field) der Instanz durch get()
        email_base, provider = email.split('@')     # Teilung der Adresse bei @
        domain, extension = provider.split('.')     # Teilung von provider
        #if not extension == "edu":                  # extension muss "edu" sein
        #    raise forms.ValidationError("Please use a valid .EDU email adress")
        return email
