from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# from .models import User

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'active', 'admin')

    def clean_password(self):
        return self.initial["password"]




class GuestForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            "class": "form-control"
        })
    )


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.TextInput(
        attrs={
            "class": "form-control"
        })
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control"
        })
    )



class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            "class": "form-control"
        })
    )
    password2 = forms.CharField(label='Password confirmation',widget=forms.PasswordInput(
        attrs={
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = ('full_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.active = False
        if commit:
            user.save()
        return user





# class RegisterForm(forms.Form):
#     username = forms.CharField(widget=forms.TextInput(
#         attrs={
#             "class": "form-control",
#             "placeholder": "Username"
#         })
#     )
#     email = forms.EmailField(widget=forms.EmailInput(
#         attrs={
#             "class": "form-control",
#             "placeholder": "Your email"
#         })
#     )
#     password = forms.CharField(widget=forms.PasswordInput(
#         attrs={
#             "class": "form-control",
#             "placeholder": "Password"
#         })
#     )
#     password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(
#         attrs={
#             "class": "form-control",
#             "placeholder": "Confirm Password"
#         })
#     )

#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         qs = User.objects.filter(username=username)
#         if qs.exists():
#             raise forms.ValidationError("Username is taken")
#         return username

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         qs = User.objects.filter(email=email)
#         if qs.exists():
#             raise forms.ValidationError("email is taken")
#         return email

#     def clean(self):
#         data = self.cleaned_data
#         password = self.cleaned_data.get('password')
#         password2 = self.cleaned_data.get('password2')

#         if password2 != password:
#             raise forms.ValidationError("Passwords must match")
#         return data
