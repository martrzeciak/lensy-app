from django import forms
from .models import CustomUser

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Napisz coś o sobie...'
            }),
        }
