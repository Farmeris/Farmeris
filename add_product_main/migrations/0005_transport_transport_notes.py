# Generated by Django 4.2.1 on 2023-06-18 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add_product_main', '0004_alter_transport_amount_alter_transport_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='transport',
            name='transport_notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
