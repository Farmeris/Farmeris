# Generated by Django 4.2.1 on 2023-06-20 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('add_product_main', '0011_additionalimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='PolozkaTransport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polozka', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_product_main.polozka')),
                ('transport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_product_main.transport')),
            ],
        ),
    ]
