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

    def clean(self):
        data = super().clean()

        # Only name check on new submits, not edits
        if not self.instance.pk:
            name = data.get('name')
            if name:
                # Don't allow same name with different cased letters
                if Profile.objects.filter(name__iexact=name):
                    msg = 'Profile with this name already exists.'
                    self.add_error('name', msg)

        return data


