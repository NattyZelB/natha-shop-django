# Generated by Django 4.2 on 2023-05-01 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_rename_varaint_value_variant_variant_value'),
        ('carts', '0002_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variants',
            field=models.ManyToManyField(blank=True, to='store.variant'),
        ),
    ]
