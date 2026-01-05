from django import forms
from .models import CustomUser

class EditProfileForm(forms.ModelForm):
    clear_avatar = forms.BooleanField(
        required=False,
        label="Usuń avatar"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'bio', 'gender', 'avatar']

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data.get('clear_avatar'):
            user.avatar = None

        if commit:
            user.save()

        return user