from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import is_safe_url
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import CreateView, FormView

from .models import Profile
from carts.models import Cart
from wishlist.models import WishList
from .forms import LoginForm, RegisterForm
from .signals import user_logged_in

from datetime import timedelta
from django.utils import timezone

from django.contrib import messages
from .utils import generate_activation_key






class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/snippets/login-form.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect("/")
        return super(LoginView, self).dispatch(*args, **kwargs)


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




def sendEmailAgain(request, data):
    if request.is_secure():
        link = "https://{host}/activate/".format(host=request.get_host())+data['activation_key']
    else:
        link = "http://{host}/activate/".format(host=request.get_host())+data['activation_key']
    message='Please click on the link below to activate your account \n\n {link} \n\n Regrads,\nTeam Onsestop'.format(link=link)
    return send_mail(
        data['email_subject'], 
        message, 
        'OneStop <no-reply@onsestop.com>', 
        [data['email']], 
        fail_silently=False
    )





def register_page(request):
    if request.user.is_authenticated():
        return redirect("/")
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
        user_detail = form.save()
        profile = Profile()
        profile.user = user_detail
        profile.activation_key = generate_activation_key(str(email))
        # profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.key_expires = timezone.now() + timedelta(days=2)
        data = {
            'activation_key': profile.activation_key,
            'email': str(user_detail),
            'email_subject': 'Activate your account'
        }
        profile.save()
        form.sendEmail(request, data)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
    return render(request, "accounts/snippets/register-form.html", context)





def activation(request, key):
    activation_expired = False
    already_active = False
    profile = get_object_or_404(Profile, activation_key=key)
    if profile.user.active == False:
        if  timezone.now() > profile.key_expires:
            activation_expired = True #Display: offer the user to send a new activation link
            id_user = profile.user.id
            profile.activation_key = generate_activation_key(str(profile.user))
            data = {
            'activation_key': profile.activation_key,
            'email': str(profile.user),
            'email_subject': 'Activate your account'
            }
            profile.save()
            sendEmailAgain(request, data)
        else: #Activation successful
            profile.user.active = True
            profile.user.save()
            profile.delete()
    #If user is already active, simply display error message
    else:
        already_active = True #Display : error message
    context = {
       "activation_expired": activation_expired 
    }
    return render(request, "accounts/snippets/activation-page.html", context)