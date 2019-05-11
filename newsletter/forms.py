from django import forms
from .models import Member

class NewsletterSubscribeForm(forms.ModelForm):
    
    class Meta:
        model = Member
        fields = ('email',)
        widgets = {
            'email': forms.TextInput(attrs={'placeholder':'Email address'})
        }


