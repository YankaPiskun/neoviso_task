from django.db import models



class Orders(models.Model):
    title = models.CharField('Заказы', max_length=50)
    clients_name = models.CharField('Имя', max_length=20)
    clients_surname = models.CharField('Фамилия', max_length=50)
    clients_car = models.CharField('Автомобиль', max_length=50)
    services = models.CharField('Услуги', max_length=50)
    employees = models.CharField('Сотрудники', max_length=50)
    orders = models.TextField('Описание')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/{self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Clients(models.Model):
    clients = models.ForeignKey(Orders, related_name='clients', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
