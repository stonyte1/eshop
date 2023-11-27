from app.models import CartProduct, User, Order, OrderProduct
from django.db.models import Sum, F
from django.utils import timezone
from dateutil.relativedelta import relativedelta


# Calculate each cart total price.
carts_total_sum = CartProduct.objects.values("cart").annotate(
    cart_sum=Sum(F("product_quantity") * F("product__price"))
)

# Get last month's users and order them by decending order.
first_day_of_this_month = timezone.now().replace(
    day=1, hour=0, minute=0, second=0, microsecond=0
)
first_day_of_last_month = first_day_of_this_month - relativedelta(months=1)
last_month_users = User.objects.filter(
    created_at__gte=first_day_of_last_month,
    created_at__lte=first_day_of_this_month,
).order_by("-email")

# Get ten biggest orders.
ten_biggest_orders = Order.objects.order_by("-order_sum")[:10]

# Calculate total sum of last month's orders.
last_month_orders_total_sum = Order.objects.filter(
    created_at__gte=first_day_of_last_month,
    created_at__lte=first_day_of_this_month,
).aggregate(Sum("order_sum"))

# Get specific user (Randall) with all his orders.
specific_user_orders = Order.objects.filter(
    user__email="mjohnson@example.org"
).order_by("-created_at")
print(specific_user_orders)

# Get users witch name start with letter j and has product 'Cup' in order.
name_from_j_users_and_cup_in_order = OrderProduct.objects.filter(
    order__user__first_name__icontains="j", product__name__icontains="Cup"
)

# Get users without orders but with products in cart.
users_with_items_in_cart_and_no_orders = User.objects.filter(
    order__isnull=True, cart__cart_product__isnull=False
).distinct()
