from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    # Bootstrap form input elements.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Profile
        fields = ['name', 'meetup', 'reddit', 'spotify', 'twitter']
