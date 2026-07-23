from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User, Profile


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number', 'full_name')

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
                raise ValidationError("رمزعبور نامعتبر است")
            return cd['password2']

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            if commit:
                user.save()
            return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(
        help_text="you cant change password using <a href =\"../password/\">this form</a>.")

    class Meta:
        model = User
        fields = ('phone_number', 'full_name', 'password', 'last_login')


class UserRegistrationForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg text-center',
            'placeholder': 'نام خود را وارد کنید'
        }))
    phone = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg text-center',
            'placeholder': 'شماره موبایل خود را وارد کنید'
        }))
        
    password = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg text-center',
            'placeholder': 'رمز عبور خود را وارد کنید'
        }))

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError("این شماره قبلا ثبت شده است")

        return phone


class UserLoginForm(forms.Form):
    phone = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg text-center',
            'placeholder': '09xxxxxxxxx'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg text-center',
            'placeholder': 'رمز عبور خود را وارد کنید'
        })
    )

class EditUserForm(forms.ModelForm):
    phone = forms.CharField(max_length=11, label='تلفن همراه')

    class Meta:
        model = Profile
        fields = ('phone', 'age', 'bio')
