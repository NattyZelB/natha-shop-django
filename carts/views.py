from django.shortcuts import render, redirect, get_object_or_404
from store.models import Products, Variant
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal

from django.http import HttpResponse


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
        return cart

def add_cart(request, product_id):
    product = Products.objects.get(id=product_id)  # get the product
    product_variant = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variant =Variant.objects.get(product=product, variant_category__iexact=key, variant_value__iexact=value)
                product_variant.append(variant)
            except:
                pass


    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))# get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        # existing _variants
        #current varaints -> product_variant
        #item_id -> database
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variant = item.variants.all()
            ex_var_list.append(list(existing_variant))
            id.append(item.id)

        if product_variant in ex_var_list:
         # increase the cart item quantity
            index = ex_var_list.index(product_variant)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variant) > 0:
                item.variants.clear()
                item.variants.add(*product_variant)# * is sure to add product_variant
            item.save()
    else:
        # create a new cart item
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        if len(product_variant) > 0:
            cart_item.variants.clear()
            cart_item.variants.add(*product_variant)
        cart_item.save()
    return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Products, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Products, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0, quantity=0,sending_cost=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += round((cart_item.product.price*cart_item.quantity)-((21*cart_item.product.price*cart_item.quantity)/100),2)
            quantity += cart_item.quantity
            tax =round((21*cart_item.product.price*cart_item.quantity)/100,2)
            if total <= 50:
                sending_cost =round(Decimal(2.99), 2)
            else:
                sending_cost = 0
            grand_total = round(total + tax + sending_cost, 2)




    except ObjectDoesNotExist:
        pass # just ignore

    context = {
        'total'       :total,
        'quantity'    : quantity,
        'cart_items'  :cart_items,
        'tax'         :tax,
        'grand_total' :grand_total,
        'sending_cost': sending_cost,

    }
    return render(request, 'store/cart.html',context)
