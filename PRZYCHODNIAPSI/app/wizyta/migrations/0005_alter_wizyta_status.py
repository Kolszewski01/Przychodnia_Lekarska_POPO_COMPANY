# Generated by Django 5.0.1 on 2024-01-13 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wizyta', '0004_alter_wizyta_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wizyta',
            name='status',
            field=models.CharField(choices=[('Oczekiwanie na wizytę', 'Oczekiwanie na wizytę'), ('Zakończono', 'Zakończono')], default='Oczekiwanie na wizytę', max_length=25),
        ),
    ]
