# Generated by Django 4.1.4 on 2024-04-14 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_remove_cart_coupon"),
        ("products", "0008_delete_userprofile"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Coupon",
        ),
    ]
