from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile, Card, Charge
from accounts.models import GuestEmail
from accounts.forms import LoginForm, GuestForm, RegisterForm
from orders.models import Order
from wishlist.models import WishList
from products.models import Product



from .models import Cart, CartItem


User_cart = settings.AUTH_USER_MODEL

STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY")



def cart_products_id(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [x.id for x in cart_obj.products.all()]
    return products



def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    request.session['cart_items'] = cart_obj.products.count()
    return render(request, "carts/home.html", {"cart": cart_obj})




def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")

    login_form = LoginForm()
    guest_form = GuestForm()
    register_form = RegisterForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_guest_profile_created = BillingProfile.objects.new_or_get(
        request)
    address_qs = None
    has_card = False
    if billing_profile is not None:
        if request.user.is_authenticated():
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)   
            del request.session["billing_address_id"]    
        if billing_address_id or shipping_address_id:
            order_obj.save()
        has_card = billing_profile.has_card

    if request.user.is_authenticated:
        temp = billing_profile.charge(order_obj)
        if temp[0]:
            order_obj.mark_paid(request, billing_profile)
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect("cart:success")

    if request.method == "POST":
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, crg_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid(request, billing_profile)
                request.session['cart_items'] = 0
                del request.session['cart_id']
                return redirect("cart:success")
            else:
                return redirect("payment_method_view")
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "register_form": register_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
    }
    return render(request, "carts/checkout.html", context)




def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})





def cart_update(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('qunatity')
    in_wishlist = False
    added = True
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except:
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cart_item_obj = CartItem.objects.new_or_get_cart_item(request, product_obj, cart_obj)
        cart_obj.products.add(cart_item_obj)

        if request.user.is_authenticated():
            wish = WishList.objects.new_or_get(request)
            wish.products.remove(product_obj)

        request.session['cart_items'] = cart_obj.products.count()
        if request.user.is_authenticated:
            billing_profile = BillingProfile.objects.filter(user=request.user)
            if billing_profile.exists():
                order_id = Order.objects.filter(billing_profile=billing_profile, status='created')
                if not order_id.exists():
                    order_obj = Order.objects.new_or_get(billing_profile[0], cart_obj)                

        if request.is_ajax():
            json_data = {
                "in_wishlist": in_wishlist,
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count(),
                "product_id": product_id
            }
        return JsonResponse(json_data)
    return redirect("cart:home")





def cart_add(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    size = request.POST.get('size')
    in_wishlist = False
    added = True
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except:
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cart_item_obj = CartItem.objects.new_or_get_cart_item(request, product_obj, cart_obj, quantity, size)
        cart_obj.products.add(cart_item_obj)

        if request.user.is_authenticated():
            wish = WishList.objects.new_or_get(request)
            wish.products.remove(product_obj)

        request.session['cart_items'] = cart_obj.products.count()
        if request.user.is_authenticated:
            billing_profile = BillingProfile.objects.filter(user=request.user)
            if billing_profile.exists():
                order_id = Order.objects.filter(billing_profile=billing_profile, status='created')
                if not order_id.exists():
                    order_obj = Order.objects.new_or_get(billing_profile[0], cart_obj)                

        if request.is_ajax():
            json_data = {
                "in_wishlist": in_wishlist,
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count(),
                "product_id": product_id
            }
        return JsonResponse(json_data)
    return redirect("cart:home")



def cart_remove(request):
    cart_item_id = request.POST.get('cart_item_id')
    cart_id = request.session.get('cart_id')

    cart_details = Cart.objects.get(id=cart_id)
    
    if cart_details.products.filter(pk=cart_item_id).exists():
        Cart.objects.get(id=cart_id).products.remove(cart_item_id)
        CartItem.objects.get(id=cart_item_id).delete()
        request.session['cart_items'] = Cart.objects.get(id=cart_id).products.count()
        json_data = {
            "removed": True,
        }
        return JsonResponse(json_data)
    else:
        return JsonResponse({'ERROR':'Item does not exist in cart'}, status=500)




def cart_detail_api_view(request):
    cart_id = request.session.get('cart_id')
    cart_details = Cart.objects.get(id=cart_id)
    products = []
    count = 0
    for x in cart_details.products.all():
        products.append({
            "id": x.item.id,
            "url": x.item.get_absolute_url(),
            "name": x.item.title,
            "price": x.calculate_total(),
            "image_url": x.item.image.url,
            "size": x.size,
            "quantity": x.quantity,
            "cart_item_id": str(x)
        })
        count = count + 1
    json_data = {
        "products": products,
        "subtotal": cart_details.subtotal, 
        "total": cart_details.total,
        "cartItemCount": count
    }
    return JsonResponse(json_data)