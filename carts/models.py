from django.db import models
from store.models import Products, Variant
class Cart(models.Model):
    cart_id =  models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.cart_id
class CartItem(models.Model):
    product   = models.ForeignKey(Products, on_delete=models.CASCADE)
    variants = models.ManyToManyField(Variant, blank=True)
    cart      = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity  = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price*self.quantity

    def __unicode__(self):
        return self.product



