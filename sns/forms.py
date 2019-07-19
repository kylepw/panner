from django import forms

from sns.models import Profile


class ProfileForm(forms.ModelForm):
    # Bootstrap form input elements.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'autofocus': ''})

    class Meta:
        model = Profile
        fields = ['name', 'meetup', 'reddit', 'spotify', 'twitter']
