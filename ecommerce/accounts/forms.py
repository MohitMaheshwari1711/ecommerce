from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.mail import send_mail

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




# class GuestForm(forms.Form):
#     email = forms.EmailField(widget=forms.TextInput(
#         attrs={
#             "class": "form-control"
#         })
#     )


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "somebody@example.com"
        })
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "placeholder": "Password"
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
            if field is 'full_name':
                self.fields[field].widget.attrs.update({
                'class': 'form-control',
                "placeholder": 'Full Name'        
            })
            if field is 'email':
                self.fields[field].widget.attrs.update({
                'class': 'form-control',
                "placeholder": 'Email'        
            })
            if field is 'password1':
                self.fields[field].widget.attrs.update({
                'class': 'form-control',
                "placeholder": 'Password'        
            })
            if field is 'password2':
                self.fields[field].widget.attrs.update({
                'class': 'form-control',
                "placeholder": 'Confirm Password'        
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
        user.active = False
        if commit:
            user.save()
        return user


    def sendEmail(self, request, data):
        if request.is_secure():
            link = "https://{host}/activate/".format(host=request.get_host())+data['activation_key']
        else:
            link = "http://{host}/activate/".format(host=request.get_host())+data['activation_key']
        # link="http://yourdomain.com/activate/"+data['activation_key']
        message='Please click on the link below to activate your account \n\n {link} \n\n Regrads,\nTeam Onsestop'.format(link=link)
        return send_mail(
            data['email_subject'], 
            message, 
            'OneStop <no-reply@onsestop.com>', 
            [data['email']], 
            fail_silently=False
        )
