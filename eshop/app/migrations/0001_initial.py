# Generated by Django 4.0.5 on 2023-10-17 07:08

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="app.category",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "categories",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="DeliveryAdress",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("country", models.CharField(max_length=60)),
                ("city", models.CharField(max_length=90)),
                ("street", models.CharField(max_length=30)),
                ("street_number", models.IntegerField()),
                ("house_number", models.IntegerField()),
                ("postal_code", models.IntegerField()),
            ],
            options={
                "verbose_name_plural": "delivery_adresses",
                "ordering": ["country"],
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("delivery_method", models.CharField(max_length=50)),
                ("delivery_status", models.CharField(max_length=20)),
                ("order_sum", models.IntegerField(default=0)),
                (
                    "delivery_adress",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="app.deliveryadress",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("price", models.IntegerField()),
                ("quantity", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="app.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("email", models.EmailField(max_length=100)),
                ("password", models.CharField(max_length=255)),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=100)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, default="", max_length=128, region=None
                    ),
                ),
                ("date_of_birth", models.DateField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.CharField(max_length=260)),
                ("image_name", models.CharField(blank=True, default="", max_length=20)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="app.product"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product_quantity", models.IntegerField()),
                ("product_price", models.IntegerField()),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.order"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="app.product"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="order",
            name="order_product",
            field=models.ManyToManyField(through="app.OrderProduct", to="app.product"),
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="app.user"
            ),
        ),
        migrations.CreateModel(
            name="CartProduct",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product_quantity", models.IntegerField()),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="app.cart"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="app.product"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="cart",
            name="cart_product",
            field=models.ManyToManyField(through="app.CartProduct", to="app.product"),
        ),
        migrations.AddField(
            model_name="cart",
            name="user_id",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.DO_NOTHING, to="app.user"
            ),
        ),
    ]
