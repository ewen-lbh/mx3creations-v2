from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField(label='Email adress', required=True, widget=forms.TextInput(attrs={'placeholder':'Email adress'}))
    message = forms.CharField(label="Your message", widget=forms.Textarea(attrs={'placeholder':'Your message'}), required=True)
    bugreport = forms.BooleanField(label="Bug report/Feature request", required=False, help_text="Are you contacting me to suggest a feature or report a bug ?")
