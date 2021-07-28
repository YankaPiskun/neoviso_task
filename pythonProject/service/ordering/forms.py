from .models import Orders
from django.forms import ModelForm, TextInput, Textarea


class OrdersForm(ModelForm):
    class Meta:
        model = Orders
        fields = ["title", "orders", "clients_name", "clients_surname", "clients_car", "services", "employees"]
        widgets = {
            "title": TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите заказ'
         }),
            "clients_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            "clients_surname": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }),
            "clients_car": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите марку машини'
            }),
            "services": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите услугу'
            }),
            "employees": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите сотрудник'
            }),


            "orders": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
            }),
        }
