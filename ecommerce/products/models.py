import random
import os
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from ecommerce.utils import unique_slug_generator

CATEGORIES = (
    ('t_shirts', 'T-Shirts'),
    ('tops', 'Tops'),
    ('casual_shirts', 'Casual Shirts'),
    ('formal_shirts', 'Formal Shirts'),
    ('sweatshirts', 'Sweatshirts'),
    ('jackets', 'Jackets'),
    ('blazzers_coats', 'Blazzers & Coats'),
    ('suits', 'Suits'),
    ('skirts', 'Skirts & Palazzos'),
    ('jeans', 'Jeans'),
    ('casual_trousers', 'Casual Trousers'),
    ('formal_trousers', 'Formal Trousers'),
    ('shorts', 'Shorts'),
    ('trackpants_joggers', 'Trackpants & Joggers'),
    ('jeggings', 'Jeggings'),
    ('capris', 'Capris'),
    ('casual_shoes', 'Casual Shoes'),
    ('formal_shoes', 'Formal Shoes'),
    ('sports_shoes', 'Sports Shoes'),
    ('sneakers', 'Sneakers'),
    ('slippers_sandals', 'Slippers & Sandals'),
    ('heels', 'Heels')
)


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 39102593125848589)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    def featured(self):
        return self.filter(featured=True, active=True)
    def search(self, query):
        lookups = Q(title__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query) | Q(tag__title__icontains=query)
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    def all(self):
        return self.get_queryset().active()
    def featured(self):
        return self.get_queryset().featured()
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
    def search(self, query):
        return self.get_queryset().active().search(query)



class Product(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    categories = models.CharField(max_length=120, choices=CATEGORIES, default='t_shirts')
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    image =  models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})
    
    def split_text(self):
        detail = self.description.split(';')
        product_detail = {
            'key_1': detail[0],
            'key_2': detail[1],
            'key_3': detail[2],
            'key_4': detail[3],
            'key_5': detail[4],
            'key_6': detail[5],
            'key_7': detail[6],
            'key_8': detail[7],
            'key_9': detail[8],
            'key_10': detail[9],
        }
        return product_detail

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)
