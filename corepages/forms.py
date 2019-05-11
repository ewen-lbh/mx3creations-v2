from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField(label='Email adress', required=True)
    message = forms.CharField(label="Your message", widgets=forms.Textarea, required=True)
    name = forms.CharField(max_length=100)
    bugreport = forms.BooleanField(label="Bug report/Feature request", required=False, help_text="Are you contacting me to suggest a feature or report a bug ?")
