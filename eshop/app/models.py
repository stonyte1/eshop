from django.db import models
import uuid
from phonenumber_field.modelfields import PhoneNumberField


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.name}"


class ProductImage(models.Model):
    image = models.CharField(max_length=260)
    image_name = models.CharField(max_length=20, blank=True, default="")
    product = models.ForeignKey("Product", on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.image}"


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name}"


class OrderProduct(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.DO_NOTHING)
    product_quantity = models.IntegerField()
    product_price = models.IntegerField()

    def __str__(self):
        return f"Order: {self.order}, product: {self.product}"


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_method = models.CharField(max_length=50)
    delivery_status = models.CharField(max_length=20)
    order_sum = models.IntegerField(default=0)
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING)
    delivery_adress = models.ForeignKey("DeliveryAdress", on_delete=models.DO_NOTHING)
    order_product = models.ManyToManyField("Product", through="OrderProduct")

    class Meta:
        ordering = ["-created_at"]

    def get_order_sum(self) -> None:
        self.order_sum = sum(
            order_product.product_quantity * order_product.product_price
            for order_product in OrderProduct.objects.filter(order=self.id)
        )

    def save(self, *args, **kwargs) -> None:
        self.get_order_sum()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}"


class DeliveryAdress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    country = models.CharField(max_length=60)
    city = models.CharField(max_length=90)
    street = models.CharField(max_length=30)
    street_number = models.IntegerField()
    house_number = models.IntegerField()
    postal_code = models.IntegerField()

    class Meta:
        ordering = ["country"]
        verbose_name_plural = "delivery_adresses"

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street}"


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(blank=True, default="")
    date_of_birth = models.DateField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email}: {self.first_name}, {self.last_name}, "


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.OneToOneField("User", on_delete=models.CASCADE)
    cart_product = models.ManyToManyField("Product", through="CartProduct")

    def __str__(self):
        return f"{self.id}"


class CartProduct(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.DO_NOTHING)
    product = models.ForeignKey("Product", on_delete=models.DO_NOTHING)
    product_quantity = models.IntegerField()

    def __str__(self):
        return f"Cart: {self.cart}, product: {self.product}"
