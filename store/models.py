from django.db import models
from django.urls import reverse

from category.models import Categories
class Products(models.Model):
    product_name    = models.CharField(max_length=50, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    color           = models.CharField(max_length=100,unique=False)
    description     = models.TextField(max_length=255, blank=True)
    price           = models.DecimalField(max_digits=5, decimal_places=2)
    images          = models.ImageField(upload_to='photos/products/', blank=True)
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Categories, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Productss'
        verbose_name_plural = 'Products'

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

class VariantManager(models.Manager):
    def colors(self):
        return super(VariantManager, self).filter(variant_category='color', is_active=True)

    def sizes(self):
        return super(VariantManager, self).filter(variant_category='size', is_active=True)

variant_category_chioce = (
    ('color', 'color'),
    ('size', 'size'),
)
class Variant(models.Model):
    product          = models.ForeignKey(Products, on_delete=models.CASCADE)
    variant_category = models.CharField(max_length=100, choices=variant_category_chioce)
    variant_value    = models.CharField(max_length=100)
    is_active        = models.BooleanField(default=True)
    created_date     = models.DateTimeField(auto_now=True)

    objects = VariantManager()

    def __str__(self):
        return self.variant_value

