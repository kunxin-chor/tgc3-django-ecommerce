from django.shortcuts import render,redirect,reverse
from .models import CartItem
from shop.models import Product
# Create your views here.

def view_cart(request):
    # reminder: request.user is the currently logged in user
    all_cart_items = CartItem.objects.filter(owner=request.user)
    return render(request, 'cart/view_cart.template.html',{
        'all_cart_items':all_cart_items
    })

def add_to_cart(request, product_id):
    
    # determine which product we are buying
    product = Product.objects.get(pk=product_id)
    
    # if the product already exists in the user's shopping cart
    existing_cart_item = CartItem.objects.filter(owner=request.user, product=product).first()
    
    # if the cart item does not exist, create a new one
    if existing_cart_item == None:
        new_cart_item = CartItem()
        new_cart_item.product = product
        new_cart_item.owner = request.user
        new_cart_item.quantity = 1
        new_cart_item.save()
    else:
        # increases its quantity
        existing_cart_item.quantity += 1
        existing_cart_item.save()
    return redirect(reverse('catalog'))
    
def remove_from_cart(request, cart_item_id):

    existing_cart_item = CartItem.objects.get(pk=cart_item_id)
    existing_cart_item.delete()
    return redirect(reverse('catalog'))