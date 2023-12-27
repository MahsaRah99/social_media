from django import forms
from .models import User
from .verification import OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] and cd["password2"] and cd["password1"] != cd["password2"]:
            raise ValidationError("passwords dont match")
        return cd["password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you can change password using <a href="../password/">this form</a>.'
    )

    class Meta:
        model = User
        fields = ("email", "username", "password", "last_login")


class UserRegistrationForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("This email already exists")
        OtpCode.objects.filter(email=email).delete()
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("This username already exists")
        return username


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "picture", "bio", "location")
