# Generated by Django 4.2.3 on 2023-08-30 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0009_userprofile_pagination_preference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='password',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='username',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='bio'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='country'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='languages',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='languages'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='location',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='location'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='phone number'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='social_media',
            field=models.URLField(blank=True, null=True, verbose_name='social media'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='state_province',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='state/province'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='street_address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='street address'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='website',
            field=models.URLField(blank=True, null=True, verbose_name='website'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='zip_postal_code',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='zip/postal code'),
        ),
    ]
