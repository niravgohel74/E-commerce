# Generated by Django 4.1.4 on 2024-04-14 08:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0010_coupon"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("accounts", "0007_remove_cart_coupon"),
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
        migrations.AlterField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="carts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
