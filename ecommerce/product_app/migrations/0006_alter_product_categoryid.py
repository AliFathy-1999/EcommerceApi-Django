# Generated by Django 3.2.18 on 2023-05-04 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0005_alter_product_categoryid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categoryId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.category'),
        ),
    ]
