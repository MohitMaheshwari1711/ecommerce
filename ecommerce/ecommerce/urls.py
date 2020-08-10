"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url, include
from django.contrib import admin
# from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from products.views import ProductListFilteredView, product_detail_api_view
from wishlist.views import get_wish_list, wish_list_remove, add_remove_wishlist, wish_list_all
from accounts.views import LoginView, register_page, guest_register_view
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from carts.views import cart_detail_api_view, cart_add, cart_remove
from billing.views import payment_method_view, payment_method_createview
from .views import home_page, about_page, contact_page

urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^about/$', about_page, name='about'),
    url(r'^contact/$', contact_page, name='contact'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', register_page, name='register'),
    url(r'^admin/', admin.site.urls),
    url(r'^register/guest/$', guest_register_view, name='guest_register'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^checkout/address/create/$', checkout_address_create_view, name='checkout_address_create'),
    url(r'^checkout/address/reuse/$', checkout_address_reuse_view, name='checkout_address_reuse'),

    url(r'^cart/', include("carts.urls", namespace="cart")),
    url(r'^api/cart/$', cart_detail_api_view, name='api-cart'),
    url(r'^api/cart/add$', cart_add, name='api-cart-add'),
    url(r'^api/cart/remove$', cart_remove, name='api-cart-remove'),

    url(r'^api/wishlist/add-remove/$', add_remove_wishlist, name='add_remove_wishlist'),
    url(r'^api/wishlist/all/$', wish_list_all, name='wish_list_all'),
    url(r'^api/wishlist/remove/$', wish_list_remove, name='wishlist_remove'),
    url(r'^wishlist/$', get_wish_list, name='wishlist_views'),

    url(r'^api/related$', product_detail_api_view, name='related-products-list'),
    url(r'^products/', include("products.urls", namespace="products")),
    url(r'^list/(?P<value>\w+)/$', ProductListFilteredView.as_view(), name='filtered_list'),
    url(r'^search/', include("search.urls", namespace="search")),

    url(r'^billing/payment$', payment_method_view, name='payment_method_view'),
    url(r'^billing/payment/create$', payment_method_createview, name='payment_method_createview'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
