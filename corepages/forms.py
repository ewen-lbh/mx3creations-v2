from django import forms
from django.utils.translation import gettext as _

class ContactForm(forms.Form):
    email = forms.EmailField(label=_('Email adress'), required=True, widget=forms.TextInput(attrs={'placeholder':_('Email adress')}))
    message = forms.CharField(label=_("Your message"), widget=forms.Textarea(attrs={'placeholder':_('Your message')}), required=True)
    bugreport = forms.BooleanField(label=_("Bug report/Feature request"), required=False, help_text=_("Are you contacting me to suggest a feature or report a bug ?"))
