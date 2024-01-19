from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth.models import User

from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput,TextInput
from .models import Item

#Register a user
class UserRegistrationForm(UserCreationForm):
    gstin = forms.CharField(max_length=15)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'gstin', 'password1', 'password2']
        def clean_gstin(self):
            gstin = self.cleaned_data['gstin']

            if len(gstin) != 15:
                raise forms.ValidationError("GSTIN must be 15 characters long.")
            if not gstin.isalnum():  
                raise forms.ValidationError("GSTIN must contain only letters and numbers.")

            if not (gstin[0:2].isalpha() and gstin[2:12].isdigit() and gstin[12:].isalpha()):
                raise forms.ValidationError("Invalid GSTIN format.")

            try:
                User.objects.get(gstin=gstin)
                raise forms.ValidationError("GSTIN already exists.")
            except User.DoesNotExist:
                pass

            return gstin
        def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords don't match")
            return password2

#login a user
class LoginForm(AuthenticationForm):
    username=forms.CharField(widget=TextInput())
    password=forms.CharField(widget=PasswordInput())
    

#create invoice
class CreateInvoice(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity', 'unit', 'rate']

#upload invoice
class ExcelFileForm(forms.Form):
    excel_file = forms.FileField()

#update invoice
class UpdateInvoice(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity', 'unit', 'rate']