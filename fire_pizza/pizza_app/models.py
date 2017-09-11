from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings


class Pizza(models.Model):
    """
    Pizza model itself.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    weight = models.PositiveSmallIntegerField()
    photo = models.ImageField(upload_to='pizza_photos')
    diameter = models.PositiveSmallIntegerField()
    price = models.PositiveSmallIntegerField()

    def __str__(self):
        return 'Pizza(name={}, diameter={})'.format(self.name, self.diameter)


class OrderItem(models.Model):
    pizza = models.ForeignKey(Pizza)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{}, quantity={}'.format(
            str(self.pizza),
            self.quantity
        )


class Order(models.Model):
    """
    Order model itself.
    """
    address = models.CharField(max_length=500)
    name = models.CharField(max_length=255)
    items = models.ManyToManyField(OrderItem, related_name='order')
    phone = models.CharField(
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'."
                    " Up to 15 digits allowed."
        )],
        max_length=16
    )
    email = models.EmailField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now=True)
    delivered = models.BooleanField(default=False)
    message = models.TextField(max_length=1000, null=True, blank=True)

    @property
    def total_price(self):
        """
        Calculates total price and adds delivery price.
        When use this -- prefetch all related data.
        """
        return sum(
            item.pizza.price * item.quantity for item in self.items.all()
        ) + settings.DELIVERY_PRICE

    def __str__(self):
        return 'Order(id={}, to={})'.format(self.id, self.address)
