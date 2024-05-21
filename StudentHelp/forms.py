from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('nom', 'prenom', 'image', 'telephone')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user = User.objects.create_user(username=user_profile.nom, password=password)
            user_profile.user = user
        if commit:
            user_profile.save()
        return user_profile


from .models import Post, Evenement

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'post_type', 'date']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if 'post_type' in self.fields:
            self.fields['post_type'].choices = [(choice[0], choice[1]) for choice in Post.POST_TYPES]
        if 'post_type' in self.initial and self.initial['post_type'] == 'Evenement':
            self.fields['subtype'] = forms.ChoiceField(choices=Evenement.EVENT_SUBTYPES)
        elif 'subtype' in self.fields:
            del self.fields['subtype']

from django import forms
from .models import TransportRequest

class TransportRequestForm(forms.ModelForm):
    class Meta:
        model = TransportRequest
        fields = ['name', 'phone_number']
