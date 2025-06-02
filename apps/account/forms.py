from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(pk__exact=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(message="Ce nom d'utilisateur est indisponible.", code="unavailable_username")
        return username
