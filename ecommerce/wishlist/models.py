from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed

from products.models import Product

User = settings.AUTH_USER_MODEL



class WishListManager(models.Manager):

    def new_or_get(self, request):
        qs = self.get_queryset().get(user=request.user)
        return qs
        

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)



class WishList(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = WishListManager()

    def __str__(self):
        return str(self.user)


