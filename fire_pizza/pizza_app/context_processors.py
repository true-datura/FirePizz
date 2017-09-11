from django.conf import settings

from .cart import Cart


def additional_context_processor(request):
    """
    Because quantity always showed near the 'Cart' button,
    better to add context processor instead of passing items quantity in
    context every time you create view.
    """
    cart = Cart(request)
    return {
        'cart_counter': cart.items_in_cart,
        'currency': settings.CURRENCY_STRING
    }
