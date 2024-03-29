# Generated by Django 3.2.24 on 2024-03-04 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='DreamCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Dream Centers',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='dream_center',
            field=models.ManyToManyField(related_name='products', to='products.DreamCenter'),
        ),
    ]
