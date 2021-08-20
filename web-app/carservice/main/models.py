from django.db import models


class Car(models.Model):
    brand = models.CharField('Марка Авто', max_length=50)

    def __str__(self):
        return self.brand

    class Meta:
        verbose_name = 'Марка Авто'
        verbose_name_plural = 'Марки Авто'


class Employee(models.Model):
    surname = models.CharField('Фамилия', max_length=70, db_index=True)
    name = models.CharField('Имя', max_length=50)
    middlename = models.CharField('Отчество', max_length=70, blank=True)

    def __str__(self):
        return self.surname

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Service(models.Model):
    turn = models.CharField('Услуга', max_length=50)

    def __str__(self):
        return self.turn

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Order(models.Model):
    clients_name = models.CharField('Имя', max_length=20)
    clients_surname = models.CharField('Фамилия', max_length=50)
    car = models.ForeignKey(Car, related_name='Авто', on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, related_name='Сотрудник', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='Услуга', on_delete=models.CASCADE)

    def __str__(self):
        return self.clients_name

    def get_absolute_url(self):
        return f'/{self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
# Create your models here.
