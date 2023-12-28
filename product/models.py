from io import BytesIO
from PIL import Image
import cv2
import numpy as np
from django.core.files import File
from django.db import models
from django.utils.text import slugify 

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = ('categories')
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    stock = models.IntegerField(max_length=6, default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/')
    thumbnail = models.ImageField(upload_to='thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True) # Added created_at
    modified_at = models.DateTimeField(auto_now=True) # Added modified_at

    def save(self, *args, **kwargs):
        if self.image:
            self.thumbnail = self.make_thumbnail(self.image)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'
    
    
    def get_image(self):
        if self.image:
            return self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return ''
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')

        pixdata = img.load()

        w, h = img.size

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                r, g, b = img.getpixel((i, j))  
                pixdata[i, j] = (r - 10, g - 10, b - 10)  

        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG')

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
