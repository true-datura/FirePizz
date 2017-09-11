from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, View, TemplateView, FormView
from django.shortcuts import redirect, get_object_or_404

from .models import Pizza, OrderItem, Order
from .forms import OrderForm
from .cart import Cart


class IndexPage(ListView):
    model = Pizza

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'main'
        return context


class CartAction(View):
    remove = False

    def get(self, request, *args, **kwargs):
        pizza_id = kwargs.get('pizza_id')
        pizza = get_object_or_404(Pizza, id=pizza_id)
        cart = Cart(request)
        if self.remove:
            cart.remove_from_cart(pizza)
        else:
            cart.add_to_cart(pizza)
        return redirect(request.GET.get('next', 'index_page'))


class FlushCart(View):
    def get(self, request, *args, **kwargs):
        Cart(request).flush_cart()
        return redirect('index_page')


class CartPage(FormView):
    template_name = 'pizza_app/cart_page.html'
    form_class = OrderForm
    success_url = reverse_lazy('index_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        context['active'] = 'cart'
        return context

    def form_valid(self, form):
        cart = Cart(self.request)

        # We can't attach any OrderItem obj if Order instance not in db
        form.instance.save()

        # Same for Order object
        items = []
        for cart_item in cart:
            order_item = OrderItem(
                pizza=cart_item['object'], quantity=cart_item['quantity']
            )
            # here can be used transaction, but I tired
            order_item.save()
            items.append(order_item)

        form.instance.items.add(*items)

        # Finally, flush cart and push the message.
        cart.flush_cart()
        messages.success(self.request, 'We will call you.')
        return super().form_valid(form)


class AdminPage(TemplateView):
    template_name = 'pizza_app/admin_page.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Authorization for pizza-admin through built-in form.
        """
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/admin/login/?next=/admin_page')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.prefetch_related('items__pizza')\
            .order_by('delivered', '-create_time').all()
        context['active'] = 'admin_page'
        return context
