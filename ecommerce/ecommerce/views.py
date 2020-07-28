from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model

from .forms import ContactForm
from products.models import Product


def home_page(request):
    queryset = Product.objects.all()
    context = {
        "title": "Home Page !!!",
        "content": "Welcome to home page",
        'home_object_list': queryset
    }
    if request.user.is_authenticated():
        context["premium_content"] = "Available"
    return render(request, "home_page.html", context)




def about_page(request):
    context = {
        "title": "About Page !!!",
        "content": "Welcome to about page"
    }
    return render(request, "home_page.html", context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact Page !!!",
        "content": "Welcome to contact page",
        "form": contact_form
    }
    if contact_form.is_valid():
        if request.is_ajax():
            return JsonResponse({
                "message": "Thank you for your submission."
            })

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')

    return render(request, "contact/view.html", context)



