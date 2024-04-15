from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .models import Profile
from products.models import *
from accounts.models import *
from django.shortcuts import get_object_or_404


# Create your views here.

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found')
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Email not verified')
            return HttpResponseRedirect(request.path_info)
        
        user_obj = authenticate(username = email, password = password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')
    return render(request, 'accounts/login.html')

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'User already exists')
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.create(first_name = first_name, last_name = last_name, email = email, username = email)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, 'An email has been sent')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/register.html')

def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token = email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except:
        return HttpResponse('Invalid Email token received')

@login_required
def add_to_cart(request, uid):
    variant = request.GET.get('variant')
    product = Product.objects.get(uid=uid)
    user = request.user
    cart , _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_item = CartItems.objects.create(cart = cart, product = product)
    # print(cart_item)
    if variant:
        variant = request.GET.get('variant')
        size_variant = SizeVariant.objects.get(size_name=variant)
        cart_item.size_variant = size_variant
        cart_item.save()
    
    profile, created = Profile.objects.get_or_create(user=user)
    if created:
        profile.save()

    cart_count = profile.get_cart_count()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER') )

def cart(request):
    cart_obj = Cart.objects.filter(is_paid=False, user = request.user).first()
    cart_item = CartItems.objects.filter(cart = cart_obj)

    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)

        if not coupon_obj.exists():
            messages.warning(request, 'Invalid coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_obj.coupon:
            messages.warning(request, 'Coupon already applied')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_obj.get_cart_total() < coupon_obj.minimum_amount:
            messages.warning(request, f'Amount should be greater than {coupon_obj.minimum_amount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if coupon_obj.is_expired:
            messages.warning(request, 'Coupon expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        cart_obj.coupon = coupon_obj
        cart_obj.save()
        messages.success(request, 'Coupon applied successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = {'cart': cart_obj, 'cart_item': cart_item}
    return render(request, 'accounts/cart.html', context)

def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid=cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_coupon(request, cart_id):
    cart = Cart.objects.get(uid = cart_id)
    cart.coupon = None
    cart.save()
    messages.success(request, 'Coupon removed successfully')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
