from django.forms import ModelForm
from .models import Event
from .models import *
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'Email (optional)'}))
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'        

class EvtProductForm(forms.ModelForm):
    class Meta:
        model = EvtProduct
        fields = '__all__'  

class CustomSetPasswordForm(SetPasswordForm):
    # Add any additional fields or customizations you may need
    pass


class EventForm(ModelForm):

    evtproducts = forms.ModelMultipleChoiceField(queryset=EvtProduct.objects.all(), widget=forms.CheckboxSelectMultiple)
  
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['transaction_id', 'payment_status', 'customer']
    
    
    
    def save(self, commit=True):
        event = super().save(commit=False)

        if commit:
            event.save()

            # Create EventItem instances for each selected product
            for chops in self.cleaned_data['evtproducts']:
                guest = int(self.cleaned_data.get('evtproducts_' + str(chops.id), 0))
                EventItem.objects.create(event=event, chops=chops, guest=guest)

        return event


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
    clear_profile_pic = forms.BooleanField(required=False)
    change_profile_pic = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        clear_profile_pic = cleaned_data.get('clear_profile_pic')
        change_profile_pic = cleaned_data.get('change_profile_pic')

        if clear_profile_pic and change_profile_pic:
            raise forms.ValidationError("You can't both clear and change the profile picture.")

        return cleaned_data

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']



class PhoneNumberResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.HiddenInput)  # Hide the email field

    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['location', 'price']

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
        

