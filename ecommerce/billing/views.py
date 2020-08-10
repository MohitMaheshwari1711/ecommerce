from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.http import JsonResponse, HttpResponse
from .models import BillingProfile, Card
from orders.models import Order
from django.conf import settings

import stripe

STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY")

stripe.api_key = STRIPE_SECRET_KEY




def payment_method_view(request):
    billing_profile = BillingProfile.objects.new_or_get(request)
    if not billing_profile[0]:
        return redirect("/cart")
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'payment-form.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})



def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return JsonResponse({ "message": "Cannot find this user" }, status=500)
        token = request.POST.get("token")
        if token is not None:
            # customer = stripe.Customer.retrieve(billing_profile[0].customer_id)
            # card_response = customer.sources.create(source=token)
            # new_card_obj = Card.objects.add_new(billing_profile[0], card_response)
            new_card_obj = Card.objects.add_new(billing_profile[0], token)
            return JsonResponse({
                "message": "Success! Your card was added.",
            })
    return JsonResponse({'message':'Payment Failed.'}, status=500)
