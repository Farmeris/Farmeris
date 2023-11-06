# Generated by Django 4.2.3 on 2023-08-04 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0002_alter_userprofile_email'),
        ('add_product_main', '0016_alter_polozkatransport_polozka_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransportLoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transport_type', models.CharField(max_length=100)),
                ('transport_notes', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=4, max_digits=20)),
                ('currency', models.CharField(max_length=3)),
                ('amount', models.DecimalField(decimal_places=5, max_digits=20)),
                ('unit', models.CharField(max_length=20)),
                ('position', models.PositiveIntegerField(default=0)),
                ('transport_name', models.CharField(blank=True, max_length=100)),
                ('polozka', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transport_locs', to='add_product_main.polozka')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login_app.userprofile')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
    ]
