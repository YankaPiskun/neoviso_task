from .models import Order
from django.forms import ModelForm, TextInput


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['clients_name', 'clients_surname', 'car', 'employee', 'service']

        widgets = {
            "clients_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            "clients_surname": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }),

        }