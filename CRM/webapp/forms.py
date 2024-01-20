from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth.models import User

from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput,TextInput
from .models import Item,GSTIN

#Register a user
class UserRegistrationForm(UserCreationForm):
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']
        
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

class CreateGst(forms.ModelForm):
    class Meta:
        model=GSTIN
        fields=['gstin_number']
    

#create invoice
class CreateInvoice(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity', 'unit', 'rate']

#upload invoice
class ExcelFileForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity', 'unit', 'rate']
    
#update invoice
class UpdateInvoice(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity', 'unit', 'rate']