from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product
from carts.models import Cart
from wishlist.models import WishList

class SearchProductView(ListView):
    template_name = "search/view.html"


    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView,
                        self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        if self.request.user.is_authenticated():
            wish_list = WishList.objects.new_or_get(self.request)
            context['wish_list'] = wish_list
        return context


    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()
