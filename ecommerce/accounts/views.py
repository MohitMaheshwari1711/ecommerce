from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import CreateView, FormView

from .models import GuestEmail
from carts.models import Cart
from wishlist.models import WishList
from .forms import LoginForm, RegisterForm, GuestForm
from .signals import user_logged_in


from django.contrib import messages

def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")
    return redirect("/register/")


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/snippets/login-form.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            wishlist_obj = WishList.objects.filter(user=request.user)
            if not wishlist_obj.exists(): 
                WishList.objects.new(user=request.user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                if Cart.objects.filter(user=request.user, active=True).exists():
                    request.session['cart_id'] = Cart.objects.get(user=request.user, active=True).id
                    request.session['cart_items'] = Cart.objects.get(user=request.user, active=True).products.count()
                return redirect("/")
        else:
            messages.error(self.request,'Login failed !!!')
        return super(LoginView, self).form_invalid(form)





def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.instance.email
        password = form.cleaned_data["password1"]
        form.save()
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
    return render(request, "accounts/snippets/register-form.html", context)
