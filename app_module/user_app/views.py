from django.shortcuts import render,redirect,HttpResponse
from app_module.admin_app import forms
from app_module.admin_app import models

from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from app_module.user_app.forms import RegisterForm

from django.contrib.auth.decorators import login_required

from app_module.admin_app import models
from django.contrib.auth.decorators import login_required
from app_module.cart_app.cart import Cart

from app_module.admin_app.models import product
from django.shortcuts import render, get_object_or_404

from django.http import JsonResponse
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay


# =========================================== Views =============================================== #

def index_view(request):
    rp = models.product.objects.all()
    context = {'rp':rp}
    return render(request,'user_app/index.html',context)

# ================================================================================================= #

def about_view(request):
    return render(request,'user_app/about.html')

# ================================================================================================= #
@login_required(login_url='pages_login')
def checkout_view(request):
    cart = Cart(request)
    
    if not cart.cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('shop_view')

    subtotal = 0
    for product_id, item in cart.cart.items():
        product_obj = models.product.objects.get(id=product_id)
        subtotal += product_obj.price * item['quantity']
    
    shipping = 500
    total = subtotal + shipping

    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        payment_method = request.POST.get('payment_method', 'Static Card')

        # Create Order
        order = models.Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            zip_code=zip_code,
            total_amount=total,
            shipping_cost=shipping,
            status='Pending'
        )

        # Create Order Items
        for product_id, item in cart.cart.items():
            product_obj = models.product.objects.get(id=product_id)
            models.OrderItem.objects.create(
                order=order,
                product=product_obj,
                quantity=item['quantity'],
                price=product_obj.price
            )

        # Determine status based on payment method
        if payment_method == 'Card':
            # Create Razorpay Order
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            amount_paise = int(total * 100)
            payment_data = {
                'amount': amount_paise,
                'currency': 'INR',
                'receipt': f"order_rcpt_{order.id}",
                'payment_capture': 1
            }
            try:
                razorpay_order = client.order.create(data=payment_data)
                razorpay_order_id = razorpay_order['id']
                
                # Create Pending Payment record
                models.Payment.objects.create(
                    order=order,
                    payment_method='Razorpay (Card)',
                    transaction_id=razorpay_order_id,
                    amount=total,
                    payment_status='Pending'
                )
                
                context = {
                    'order': order,
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                    'total_amount_paise': amount_paise,
                }
                return render(request, 'user_app/razorpay_payment.html', context)
            except Exception as e:
                messages.error(request, f"Razorpay order creation failed: {str(e)}")
                order.status = 'Cancelled'
                order.save()
                return redirect('checkout_view')
        else:
            # Cash on Delivery
            transaction_id = f"FB-{uuid.uuid4().hex[:8].upper()}"
            models.Payment.objects.create(
                order=order,
                payment_method=payment_method,
                transaction_id=transaction_id,
                amount=total,
                payment_status='Pending'
            )
            order.status = 'Pending'
            order.save()
            cart.clear()
            messages.success(request, f"Order placed successfully! Transaction ID: {transaction_id}")
            return redirect('invoice_view', order_id=order.id)

    cart_items = []
    for product_id, item in cart.cart.items():
        product_obj = models.product.objects.get(id=product_id)
        cart_items.append({
            'product': product_obj,
            'quantity': item['quantity'],
            'item_total': product_obj.price * item['quantity']
        })

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total
    }

    return render(request, 'user_app/checkout.html', context)

@login_required(login_url='pages_login')
def invoice_view(request, order_id):
    order = get_object_or_404(models.Order, id=order_id, user=request.user)
    payment = models.Payment.objects.get(order=order)
    context = {
        'order': order,
        'payment': payment
    }
    return render(request, 'user_app/invoice.html', context)

# ================================================================================================= #
@csrf_exempt
def razorpay_callback(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        order_id = request.POST.get('order_id')
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        try:
            # Verify signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            client.utility.verify_payment_signature(params_dict)
            
            # Fetch the order and update status
            order = get_object_or_404(models.Order, id=order_id)
            order.status = 'Processing'
            order.save()
            
            # Update Payment record
            payment, created = models.Payment.objects.get_or_create(order=order)
            payment.payment_method = 'Razorpay (Card)'
            payment.transaction_id = razorpay_payment_id
            payment.payment_status = 'Success'
            payment.save()
            
            # Clear cart
            cart = Cart(request)
            cart.clear()
            
            messages.success(request, f"Payment successful! Order processed. Transaction ID: {razorpay_payment_id}")
            return redirect('invoice_view', order_id=order.id)
            
        except Exception as e:
            messages.error(request, f"Payment verification failed: {str(e)}")
            return redirect('checkout_view')
            
    return redirect('checkout_view')

# ================================================================================================= #

def contact_view(request):
    if request.method == 'POST':
        form = forms.contectdata(request.POST)
        if form.is_valid():
            contact = form.save()
            # Trigger notification
            models.Notification.objects.create(message=f"New contact message from {contact.name}")
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact_view')
        else:
            print(form.errors)
    return render(request,'user_app/contact.html')

# ================================================================================================= #

def fzf_view(request):
    return render(request,'user_app/fzf.html')

# ================================================================================================= #

def news_view(request):
    return render(request,'user_app/news.html')

# ================================================================================================= #

def shop_view(request):
    search = request.GET.get('search')
    category_id = request.GET.get('category')

    products = models.product.objects.all()

    # search filter
    if search:
        products = products.filter(name__icontains=search)

    # category filter
    if category_id:
        products = products.filter(category_id=category_id)

    category = models.category.objects.all()
    context = {'P':products,'category':category}

    return render(request, 'user_app/shop.html', context)

# ================================================================================================= #

def single_news_view(request):
    if request.method == 'POST':
        form = forms.commentsdata(request.POST)
        if form.is_valid():
            form.save()
            return redirect(single_news_view)
        else:
            print(form.errors)
    return render(request,'user_app/single_news.html')

# ================================================================================================= #

def single_product_view(request, id):
    product_obj = get_object_or_404(product, id=id)
    reviews = product_obj.reviews.all().order_by('-created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Please login to leave a review.")
            return redirect('pages_login')
            
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')
        
        if rating and review_text:
            models.ProductReview.objects.create(
                product=product_obj,
                user=request.user,
                rating=rating,
                review_text=review_text
            )
            messages.success(request, "Thank you for your review!")
            return redirect('single_product_view', id=id)

    context = {
        'product': product_obj,
        'reviews': reviews,
    }
    return render(request, 'user_app/single_product.html', context)

# ================================================================================================= #

def subscribe_view(request):
    if request.method == 'POST':
        form = forms.subscribedata(request.POST)
        if form.is_valid():
            form.save()
    return redirect(request.META.get('HTTP_REFERER'))

# ================================================================================================= #

# :: REGISTER & LOGIN ::
def pages_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check password match
        if password1 != password2:
            return HttpResponse("Password Do Not Match!!")

        # Check username exists
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username Already Exists Please Try Again")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        
        # Create notification for admin
        models.Notification.objects.create(message=f"New user registered: {user.username}")
        messages.success(request, "Registration successful! You can now login.")

        return redirect('pages_login')

    return render(request,'user_app/pages_register.html')

def pages_login(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            status, created = models.UserStatus.objects.get_or_create(user=user)

            # ✅ CHECK BLOCK FIRST
            if status.is_blocked:
                messages.error(request, "Your account is blocked by the administrator.")
                return redirect('pages_login')

            # ✅ THEN LOGIN
            login(request, user)
            status.is_online = True
            status.save()

            messages.success(request, f"Welcome back, {user.username}!")

            # ✅ ROLE-BASED REDIRECTION
            if user.is_superuser:
                return redirect('admin_app:index')
            else:
                return redirect('index_view')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('pages_login')
        
    return render(request, 'user_app/pages_login.html')

def logout_view(request):

    if request.user.is_authenticated:
        status = models.UserStatus.objects.get(user=request.user)
        status.is_online = False
        status.save()

    logout(request)
    return redirect('index_view')

# ================================================================================================= #

def auth_base_view(request):
    return render(request,'user_app/auth_base.html')

# ================================================================================================= #

# @login_required(login_url="/users/login")
def cart_add(request, id):
    cart = Cart(request)
    product = models.product.objects.get(id=id)
    cart.add(product=product)

    total_quantity = sum(item['quantity'] for item in cart.cart.values())

    return JsonResponse({'cart_total_quantity': total_quantity})


@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = models.product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_view")


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = models.product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_view")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = models.product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_view")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("item_clear")


# @login_required(login_url="/users/login")
# def cart_detail(request):
#     return render(request, 'user_app/cart_detail.html')


@login_required(login_url='cart_view')
def cart_view(request):
    cart = Cart(request)
    cart_items = []
    subtotal = 0

    for product_id, item in cart.cart.items():
        product = models.product.objects.get(id=product_id)
        quantity = item['quantity']
        item_total = product.price * quantity
        subtotal += item_total

        cart_items.append({ 'product': product, 'quantity': quantity,'item_total': item_total })

    shipping = 500
    total = subtotal + shipping

    context = {'cart_items': cart_items, 'subtotal': subtotal, 'shipping': shipping, 'total': total }

    return render(request, 'user_app/cart.html', context)

# ================================================================================================= #
