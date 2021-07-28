# Generated by Django 3.2.5 on 2021-07-18 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='ordering.orders')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
    ]