from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseServerError
from django.conf import settings
# from accounts.models import GuestEmail

from products.models import Product
from carts.models import Cart
from billing.models import BillingProfile
from .models import WishList


User_cart = settings.AUTH_USER_MODEL



def get_wish_list(request):
    wish_list = WishList.objects.filter(user=request.user).first()
    queryset = wish_list.products.all()
    context = {
        'wish_list': queryset
    }
    return render(request, "home.html", context)


def wish_list_all(request):
    if request.user.is_authenticated():
        wish_list = WishList.objects.new_or_get(request)
        products = [{
            "id": x.id,
            "url": x.get_absolute_url(),
            "name": x.title,
            "price": x.price,
            "image_url": x.image.url
            } for x in wish_list.products.all()]

        json_data = {
            "products": products
        }
        return JsonResponse(json_data)
    





def add_remove_wishlist(request):
    if request.user.is_authenticated():
        product_id = request.POST.get('product_id')
        if product_id is not None:
            try:
                product_obj = Product.objects.get(id=product_id)
            except:
                return redirect("products:list")
            wishlist = WishList.objects.new_or_get(request)
            if product_obj in wishlist.products.all():
                wishlist.products.remove(product_obj)
                added = False
            else:
                wishlist.products.add(product_obj)
                added = True

            if request.is_ajax():
                json_data = {
                    "added": added
                }
                return JsonResponse(json_data)
    else:
        return JsonResponse({'ERROR':'Please login first !!!'}, status=500)





def wish_list_remove(request):
    product_id = request.POST.get('product_id')
    wish_list = WishList.objects.new_or_get(request)
    wish_list.products.remove(product_id)
    products = [{
        "id": x.id,
        "url": x.get_absolute_url(),
        "name": x.title,
        "price": x.price,
        "image_url": x.image.url
        } for x in wish_list.products.all()]
    remove = True 
    if Cart.objects.filter(user=request.user, active=True).count() == 0:    
        json_data = {
            "removed": remove,
            "products": products,
            "count": 0
        }
    else:
        json_data = {
            "removed": remove,
            "products": products,
            "count": Cart.objects.get(user=request.user, active=True).products.count()
        }
    return JsonResponse(json_data)
