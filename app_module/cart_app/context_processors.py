from .cart import Cart

def cart_total_amount(request):
    cart = Cart(request)

    total_quantity = 0

    for item in cart.cart.values():
        total_quantity += item.get('quantity', 0)

    return {
        'cart_total_quantity': total_quantity,
    }
