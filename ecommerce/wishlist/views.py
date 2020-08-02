from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from accounts.models import GuestEmail

from products.models import Product
from carts.models import Cart
from billing.models import BillingProfile
from .models import WishList


User_cart = settings.AUTH_USER_MODEL

# Create your views here.



# def wishlist_api_view(request):
#     wish_list = WishList.objects.filter(user=request.user).first()
#     print(wish_list)
#     products = [{
#         "id": x.id,
#         "url": x.get_absolute_url(),
#         "name": x.title,
#         "price": x.price,
#         "image_url": x.image.url
#         } for x in wish_list.products.all()]
#     wish_list_data = {"products": products}
#     return JsonResponse(wish_list_data)



def get_wish_list(request):
    wish_list = WishList.objects.filter(user=request.user).first()
    queryset = wish_list.products.all()
    context = {
        'wish_list': queryset
    }
    return render(request, "home.html", context)



def wish_list_update(request):
    product_id = request.POST.get('product_id')    
    product_obj = Product.objects.get(id=product_id)
    cart_obj = Cart.objects.new_or_get(request)
    wish_list = WishList.objects.new_or_get(request)
    wish_list.products.remove(product_id)
    products = [{
        "id": x.id,
        "url": x.get_absolute_url(),
        "name": x.title,
        "price": x.price,
        "image_url": x.image.url
        } for x in wish_list.products.all()]
    if product_obj in Cart.objects.get(user=request.user, active=True).products.all():
        added = True
        json_data = {
            "added": added,
            "removed": not added,
            "exists_in_cart": True,
            "products": products,
            "count": Cart.objects.get(user=request.user, active=True).products.count()
        }
    else:
        Cart.objects.get(user=request.user, active=True).products.add(product_obj)
        added = True
        json_data = {
            "added": added,
            "removed": not added,
            "exists_in_cart": False,
            "products": products,
            "count": Cart.objects.get(user=request.user, active=True).products.count()
        }

    return JsonResponse(json_data)
            