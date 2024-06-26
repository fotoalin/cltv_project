# Generated by Django 5.0.6 on 2024-06-01 21:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cltv_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CLTVResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cltv', models.DecimalField(decimal_places=2, max_digits=10)),
                ('calculated_at', models.DateTimeField(auto_now_add=True)),
                ('customer_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cltv_app.customerdata')),
            ],
        ),
    ]
