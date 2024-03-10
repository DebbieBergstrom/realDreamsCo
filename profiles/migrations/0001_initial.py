# Generated by Django 3.2.24 on 2024-03-10 16:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('default_street_address1', models.CharField(blank=True, max_length=80, null=True)),
                ('default_street_address2', models.CharField(blank=True, max_length=80, null=True)),
                ('default_town_or_city', models.CharField(blank=True, max_length=40, null=True)),
                ('default_county', models.CharField(blank=True, max_length=80, null=True)),
                ('default_postcode', models.CharField(blank=True, max_length=20, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('preferred_contact_method', models.CharField(choices=[('EMAIL', 'Email'), ('PHONE', 'Phone')], default='EMAIL', max_length=10, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('preferred_dreamcenter', models.CharField(choices=[('STOCKHOLM', 'Stockholm'), ('BERLIN', 'Berlin'), ('PARIS', 'Paris')], default='STOCKHOLM', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HealthStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_epilepsy', models.BooleanField(default=False, verbose_name='Do you have epilepsy?')),
                ('has_heart_conditions', models.BooleanField(default=False, verbose_name='Do you have any heart conditions?')),
                ('has_mental_illness', models.BooleanField(default=False, verbose_name='Do you have any mental illnesses?')),
                ('suffers_from_ptsd', models.BooleanField(default=False, verbose_name='Do you suffer from PTSD?')),
                ('additional_information', models.TextField(blank=True, verbose_name='Anything else we need to know prior a realDream session?')),
                ('last_updated', models.DateTimeField(auto_now_add=True, verbose_name='Last Updated')),
                ('declaration_truthful', models.BooleanField(default=False, verbose_name='I confirm that the information provided is true and accurate to the best of my knowledge.')),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='health_status', to='profiles.userprofile')),
            ],
            options={
                'verbose_name': 'Health Status',
                'verbose_name_plural': 'Health Status Declarations',
            },
        ),
    ]
