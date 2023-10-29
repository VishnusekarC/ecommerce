import razorpay
from carts.models import Cart
from payments.models import Payment

from .models import Order, OrderItem
from ecommerce.settings import RAZOR_PAY_KEY_ID, RAZOR_PAY_KEY_SECRET


def create_order(cart: Cart, user) -> Order:
    order = dict()

    order['user'] = cart.user
    order['address'] = cart.address
    order['shipping_price'] = cart.get_shipping_price
    order['discount'] = cart.discount
    order['coupon_code'] = cart.coupon_code
    order['cart_id'] = cart.id
    order['total'] = cart.get_total
    order['tax'] = cart.get_tax_amount
    order['grand_total'] = cart.get_total_payable

    order = Order.objects.create(**order)

    order_item_objects = []
    for item in cart.cart_items.all():
        order_item_objects.append(
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
        )
    OrderItem.objects.bulk_create(order_item_objects)
    return order


client = razorpay.Client(auth=(RAZOR_PAY_KEY_ID, RAZOR_PAY_KEY_SECRET))


def create_payment_for_order(order: Order):
    try:
        payment = Payment.objects.get(order=order)
    except Payment.DoesNotExist:
        data = {
            "amount": int(order.grand_total * 100),
            "currency": "INR",
            "receipt": f"#{order.id}"
            }
        rzp_payment = client.order.create(data=data)
        payment = Payment()
        payment.order = order
        payment.total=order.grand_total
        payment.rzp_order_id=rzp_payment.get('id')
        payment.raw_data = rzp_payment
        payment.save(force_insert=True)
    return payment
    
