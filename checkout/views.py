from django.shortcuts import render, HttpResponse
from .forms import OrderForm, PaymentForm
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from cart.models import CartItem
import stripe


def calculate_cart_cost(request):
    all_cart_items = CartItem.objects.filter(owner=request.user)
    amount = 0
    for cart_item in all_cart_items:
        amount += cart_item.product.cost * cart_item.quantity
        
    return amount

# Create your views here.
def checkout(request):
    total_cost = calculate_cart_cost(request)
   
        
    return render(request, 'checkout/checkout.template.html', {
        'total_cost':total_cost/100
    })
    
def charge(request):
    amount = calculate_cart_cost(request)
    
    if request.method == 'GET':
        order_form = OrderForm()
        payment_form = PaymentForm()
        return render(request, 'checkout/charge.template.html', {
            'order_form' : order_form,
            'payment_form' : payment_form,
            'amount' : amount,
            'publishable': settings.STRIPE_PUBLISHABLE_KEY
        })
    else:
        stripeToken = request.POST['stripe_id']
        
        # set the secret key for the Stripe API
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        order_form = OrderForm(request.POST)
        payment_form = PaymentForm(request.POST)
        
        if order_form.is_valid() and payment_form.is_valid():
            try:
                customer = stripe.Charge.create(
                    amount= int(request.POST['amount'])*100,
                    currency='usd',
                    description='Donation',
                    card=stripeToken
                    )
                    
                if customer.paid:
                    
                    order = order_form.save(commit=False)
                    order.date=timezone.now()
                    order.save()
                    
                    return render(request, 'checkout/thankyou.template.html')
                else:
                    messages.error(request, "Your card has been declined")
            except stripe.error.CardError:
                    messages.error(request, "Your card was declined!")
            
        else:
             return render(request, 'checkout/charge.template.html', {
            'order_form' : order_form,
            'payment_form' : payment_form,
            'amount' : amount,
            'publishable': settings.STRIPE_PUBLISHABLE_KEY
        })
        
        return render(request, 'checkout/charge.template.html', {
            'order_form' : order_form,
            'payment_form' : payment_form,
            'amount' : amount,
            'publishable': settings.STRIPE_PUBLISHABLE_KEY
            })