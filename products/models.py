from django.db import models
from datetime import datetime
import os
import random
from django.db.models.signals import pre_save
from hascoffee.utils import unique_slug_generator
from django.urls import reverse
from django.db.models.aggregates import Count
from random import randint

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    date_time = datetime.now()
    formatedDate = date_time.strftime("%Y-%m-%d")
    title = instance.title.replace(" ", "")
    new_filename = random.randint(1, 5000000)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{date_time}/{title}/{final_filename}".format(date_time=formatedDate, title=title, final_filename=final_filename)

class ProductManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]

class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    country = models.CharField(max_length=100)
    ingridients = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=9.99) #null - empty in the DB
    drying_method = models.CharField(max_length=100, blank=True)
    drying_time = models.IntegerField(blank=True, null=True)
    photo_main = models.ImageField(upload_to=upload_image_path)
    photo_1 = models.ImageField(upload_to=upload_image_path, blank=True)
    photo_2 = models.ImageField(upload_to=upload_image_path, blank=True)
    photo_3 = models.ImageField(upload_to=upload_image_path, blank=True)
    photo_4 = models.ImageField(upload_to=upload_image_path, blank=True)
    photo_5 = models.ImageField(upload_to=upload_image_path, blank=True)
    item_sold = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=datetime.now)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return "/products/{slug}".format(slug=self.slug) # hard-coded return
        return reverse("product_detail", kwargs={"slug": self.slug})

def listing_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(listing_pre_save_receiver, sender=Product)
