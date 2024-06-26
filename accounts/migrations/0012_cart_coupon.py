# Generated by Django 4.1.4 on 2024-04-14 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0016_coupon"),
        ("accounts", "0011_remove_cart_coupon"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="coupon",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="coupons",
                to="products.coupon",
            ),
        ),
    ]
