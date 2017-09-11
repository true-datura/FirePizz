from django.conf import settings

from .models import Pizza


class Cart:
    """
    Session-based cart.
    """
    def __init__(self, request):
        """
        Initialize cart in session.
        """
        self.session = request.session
        self.cart_id = settings.CART_SESSION_ID
        self.cart = self.session.setdefault(self.cart_id, {})

    def add_to_cart(self, pizza):
        """
        Adds an item in cart.
        """
        pizza_id = str(pizza.id)
        if pizza_id not in self.cart:
            self.cart[pizza_id] = {'quantity': 1, 'price': pizza.price}
        else:
            self.cart[pizza_id]['quantity'] += 1
        self.save()

    def remove_from_cart(self, pizza):
        """
        Decrements pizza quantity or deletes it from cart.
        """
        pizza_id = str(pizza.id)

        if pizza_id in self.cart:
            if self.cart[pizza_id]['quantity'] > 1:
                self.cart[pizza_id]['quantity'] -= 1
            else:
                del self.cart[pizza_id]

            self.save()

    def flush_cart(self):
        """
        Removes all items from cart.
        """
        self.cart = {}
        self.save()

    def save(self):
        """
        Updates cart in session.
        """
        self.session[self.cart_id] = self.cart
        self.session.modified = True

    def total_price(self):
        return sum(
            pizza['price'] * pizza['quantity'] for pizza in self.cart.values()
        ) + settings.DELIVERY_PRICE

    @property
    def items_in_cart(self):
        """How much items in cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        # first, place original objects in self.cart with some additional
        # information
        pizzas = Pizza.objects.filter(id__in=self.cart.keys())
        for pizza in pizzas:
            self.cart[str(pizza.id)]['object'] = pizza
            self.cart[str(pizza.id)]['total_price'] = \
                self.cart[str(pizza.id)]['quantity'] * pizza.price

        # then return iterator
        # could be done through __next__ and counter, but I think it's
        # better.
        for pizza in sorted(self.cart.values(), key=lambda x: x['quantity']):
            yield pizza

    def __bool__(self):
        """
        Cute way to check if cart is empty from template.
        """
        return bool(self.cart)
