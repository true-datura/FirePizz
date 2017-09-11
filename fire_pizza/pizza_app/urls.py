from django.conf.urls import url

from .views import IndexPage, CartAction, CartPage, FlushCart, AdminPage

urlpatterns = [
    url(r'^$', IndexPage.as_view(), name='index_page'),
    url(r'^cart/$', CartPage.as_view(), name='cart_page'),
    url(r'^cart/(?P<pizza_id>\d+)/$', CartAction.as_view(),
        name='add_to_cart'),
    url(r'^cart/(?P<pizza_id>\d+)/remove/$', CartAction.as_view(remove=True),
        name='remove_from_cart'),
    url(r'^cart/flush/$', FlushCart.as_view(), name='flush_cart'),
    url(r'^admin_page/$', AdminPage.as_view(), name='admin_page'),
]
