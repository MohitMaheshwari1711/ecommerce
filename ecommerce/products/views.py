from django.http import Http404, JsonResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from analytics.mixins import ObjectViewedMixin
from carts.models import Cart
from .models import Product

from carts.views import cart_products_id

product_id = None



class ProductFeaturedListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
    template_name = "products/featured-detail.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


class ProductListView(ListView):
    template_name = "products/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(
            *args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView,
                        self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        global product_id
        try:
            instance = Product.objects.get(slug=slug, active=True)
            product_id = instance.id
        except Product.DoesNotExist:
            raise Http404("Not Found...")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
            product_id = instance.id
        except:
            raise Http404("Hmmm...")
        return instance


def product_detail_api_view(request):
    global product_id
    caegory = Product.objects.get(id=product_id).categories
    products = []
    cart_productsID = cart_products_id(request)
    for x in Product.objects.all().exclude(id=product_id).filter(categories=caegory):
        if products.__len__() < 4:
            if x.id not in cart_productsID:
                products.append({
                    "id": x.id,
                    "url": x.get_absolute_url(),
                    "name": x.title,
                    "price": x.price,
                    "image_url": x.image.url
                })
        else:
            break
    return JsonResponse({"products": products})


class ProductListFilteredView(ListView):
    template_name = "products/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListFilteredView,
                        self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all().filter(categories=self.kwargs.get('value'))


class ProductDetailView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise htt404("Product doesn't exist")
        return instance


def product_detail_view(request, pk=None, *args, **kwargs):
    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise htt404("Product doesn't exist")
    context = {
        'object': instance
    }
    return render(request, "products/detail.html", context)
