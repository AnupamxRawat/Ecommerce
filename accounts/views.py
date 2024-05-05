from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Cartitems
# Create your views here.
from accounts.models import Cart,Cartitems
from products.models import SizeVariant,ColorVariant,Coupon
from django.http import HttpResponseRedirect
from products.models import Product

from django.views.decorators.csrf import csrf_exempt


import razorpay 
from django.conf import settings

def login_page(request):
    if request.method =='POST':
        email =request.POST.get('email')
        password =request.POST.get('password')

        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)
        
        '''if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Account not verified.')
            return HttpResponseRedirect(request.path_info)'''

        user_obj= authenticate(username=email,password= password)

        if user_obj:
            login(request, user_obj)
            messages.success(request, 'Success')
            return redirect('/')

        messages.warning(request, 'Invalid Credentials')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/login.html') 

def register_page(request):
    if request.method =='POST':
        first_name =request.POST.get('first_name')
        last_name =request.POST.get('last_name')
        email =request.POST.get('email')
        password =request.POST.get('password')

        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)
    
    return render(request, 'accounts/register.html')
    

def add_to_cart(request, uid):
    try:
        variant = request.GET.get('variant')
        product = Product.objects.get(uid=uid)
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
        cart_item = Cartitems.objects.create(cart=cart, product=product)
        
        # Check if a size variant is selected and associate it with the cart item
        if variant:
            size_variant = SizeVariant.objects.get(size_name=variant)
            cart_item.size_variant = size_variant
            cart_item.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print(e) 


def remove_cart(request,cart_item_uid):
    try:
        cart_item=Cartitems.objects.get(uid=cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e) 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
def cart(request):
    cart_obj=None
    try:
     cart_obj=Cart.objects.get(is_paid=False,user=request.user)
    
    except Exception as e: 
     if request.method =='POST':
       
        coupon= request.POST.get('coupon')
        coupon_obj=Coupon.objects.filter(coupon_code__icontains=coupon).first()
        if not coupon_obj:
            messages.warning(request,'Coupon does not exist')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_obj.get_cart_total() < coupon_obj.minimum_amount:
            messages.warning(request,f'Amount should be more than {coupon_obj.minimum_amount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if coupon_obj.is_expired:
            messages.warning(request,f'Coupon expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_obj.coupon:
            messages.warning(request,'Coupon already applied')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        cart_obj.coupon=coupon_obj
        cart_obj.save()
        messages.success(request,'Coupon applied.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    if cart_obj:
        client=razorpay.Client(auth=(settings.KEY , settings.SECRET))
        payment= client.order.create({'amount':cart_obj.get_cart_total()*100,'currency':'INR','payment_capture':1})
        cart_obj.razor_pay_payment_id=payment['id']
        cart_obj.save()
        print('******')
        print(payment)
        print('******')
    else:
     payment=None
    context={'cart': cart_obj,'payment':payment}
    return render(request,'accounts/cart.html',context)


def remove_coupon(request,cart_id):

    cart=Cart.objects.get(uid =cart_id)
    cart.coupon=None
    cart.save()
    messages.success(request,'Coupon removed.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def success(request):
    order_id = request.GET.get('order_id')
    order = Cart.objects.get(razor_pay_payment_id=order_id)  # Retrieve order details
    # Pass order details to the invoice template
    context = {'order': order}
    # Render the invoice template with the order details
    return render(request, 'pdfs/invoice.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Cart
from django.template.loader import get_template

def invoice(request):
    user_cart = Cart.objects.filter(user=request.user, is_paid=True).first()
    
    # Render the invoice HTML
    template = get_template('pdfs/invoice.html')
    context = {'cart': user_cart}
    html = template.render(context)
    return HttpResponse(html)