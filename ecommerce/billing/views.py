from django.shortcuts import render
from django.utils.http import is_safe_url
from django.http import JsonResponse, HttpResponse

import stripe

STRIPE_PUB_KEY = "*********************************"



def payment_method_view(request):
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'payment-form.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})



def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        print(request.POST)
        return JsonResponse({
            "message": "Success! Your card was added."
        })
    return JsonResponse({'message':'Payment Failed.'}, status=500)
