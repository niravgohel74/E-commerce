# Generated by Django 5.0.4 on 2024-04-18 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0012_cart_coupon"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="razorpay_order_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="cart",
            name="razorpay_payment_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="cart",
            name="razorpay_signature_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
