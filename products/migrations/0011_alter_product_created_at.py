# Generated by Django 3.2.12 on 2024-07-22 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_productcategory_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
