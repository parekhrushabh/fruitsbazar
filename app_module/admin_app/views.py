from django.shortcuts import render, HttpResponse, redirect
from app_module.admin_app import models
from app_module.admin_app import forms
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages

from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.utils import timezone
import datetime


# =========================================== Views ======================================#

# :: INDEX ::
def index(request):

    total_product = models.product.objects.count() 
    total_category = models.category.objects.count() 
    total_contacts = models.contect.objects.count() 
    total_subscribers = models.subscribe.objects.count()
    total_users = User.objects.count() 
    
    # Order & Revenue Stats
    total_orders = models.Order.objects.count()
    
    # Detailed Payment Summary Stats
    payments = models.Payment.objects.all()
    total_payments_count = payments.count()
    
    success_payments = payments.filter(payment_status='Success')
    success_payments_count = success_payments.count()
    total_revenue = success_payments.aggregate(Sum('amount'))['amount__sum'] or 0
    
    pending_payments = payments.filter(payment_status='Pending')
    pending_payments_count = pending_payments.count()
    total_pending_amount = pending_payments.aggregate(Sum('amount'))['amount__sum'] or 0
    
    failed_payments = payments.filter(payment_status='Failed')
    failed_payments_count = failed_payments.count()
    total_failed_amount = failed_payments.aggregate(Sum('amount'))['amount__sum'] or 0
    
    payment_success_rate = round((success_payments_count / total_payments_count * 100), 1) if total_payments_count > 0 else 0
    
    # Successful Payment breakdown by method (for visual stats)
    cod_success_amount = success_payments.filter(payment_method__icontains='COD').aggregate(Sum('amount'))['amount__sum'] or 0
    online_success_amount = success_payments.exclude(payment_method__icontains='COD').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Total counts by method (for method pie chart)
    cod_count = payments.filter(payment_method__icontains='COD').count()
    online_count = payments.exclude(payment_method__icontains='COD').count()
    
    recent_orders = models.Order.objects.all().order_by('-id')[:5]
    recent_payments = payments.order_by('-id')[:5]

    # Generate Report Chart Data for the last 7 days
    chart_dates = []
    sales_data = []
    revenue_data = []
    customers_data = []
    
    today = timezone.localdate()
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        chart_dates.append(date.strftime("%Y-%m-%d"))
        
        # Count orders created on this day
        sales_count = models.Order.objects.filter(created_at__date=date).count()
        sales_data.append(sales_count)
        
        # Sum revenue (successful payments) received on this day
        rev_sum = models.Payment.objects.filter(created_at__date=date, payment_status='Success').aggregate(Sum('amount'))['amount__sum'] or 0
        revenue_data.append(float(rev_sum))
        
        # Count customer registrations on this day
        cust_count = User.objects.filter(date_joined__date=date).count()
        customers_data.append(cust_count)

    # Dynamic Activity (Latest 6 items across different models)
    recent_activity = []
    for order in models.Order.objects.all().order_by('-id')[:3]:
        recent_activity.append({'type': 'order', 'message': f'New Order #{order.id} from {order.full_name}', 'time': order.created_at})
    for contact in models.contect.objects.all().order_by('-id')[:3]:
        recent_activity.append({'type': 'contact', 'message': f'New Message from {contact.name}', 'time': contact.id}) # Simulating time with ID or just using order
    
    # Notifications
    notifications = models.Notification.objects.filter(is_read=False).order_by('-id')[:5]
    total_notifications = models.Notification.objects.filter(is_read=False).count()

    recent_products = models.product.objects.all().order_by('-id')[:5]
    recent_contact = models.contect.objects.all().order_by('-id')[:5]

    # Dynamic Website Traffic calculation based on database records scale
    traffic_search = total_users * 25 + total_orders * 15 + 125
    traffic_direct = total_orders * 20 + total_contacts * 10 + 80
    traffic_email = total_subscribers * 15 + 50
    traffic_referral = models.ProductReview.objects.count() * 12 + total_product * 5 + 40
    traffic_other = total_category * 10 + total_contacts * 5 + 30

    context = {
        'total_product': total_product, 
        'total_category': total_category, 
        'total_contacts': total_contacts, 
        'total_contact': total_contacts, # Support both template name variations
        'total_subscribers': total_subscribers, 
        'recent_products': recent_products, 
        'recent_contact': recent_contact, 
        'total_users': total_users,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'recent_activity': recent_activity,
        'notifications': notifications,
        'total_notifications': total_notifications,
        # Chart data
        'chart_dates': chart_dates,
        'sales_data': sales_data,
        'revenue_data': revenue_data,
        'customers_data': customers_data,
        # Payment detailed stats
        'total_payments_count': total_payments_count,
        'success_payments_count': success_payments_count,
        'pending_payments_count': pending_payments_count,
        'failed_payments_count': failed_payments_count,
        'total_pending_amount': total_pending_amount,
        'total_failed_amount': total_failed_amount,
        'payment_success_rate': payment_success_rate,
        'cod_success_amount': float(cod_success_amount),
        'online_success_amount': float(online_success_amount),
        'cod_count': cod_count,
        'online_count': online_count,
        'recent_payments': recent_payments,
        # Dynamic Traffic Stats
        'traffic_search': traffic_search,
        'traffic_direct': traffic_direct,
        'traffic_email': traffic_email,
        'traffic_referral': traffic_referral,
        'traffic_other': traffic_other,
    }
    
    return render(request,'admin_app/index.html',context)

#=========================================================================================#
# :: REGISTER & LOGIN ::


#=========================================================================================#
# :: COMPONENTS ::
def components_alerts(request):
    return render(request,'admin_app/components_alerts.html')
def components_accordion(request):
    return render(request,'admin_app/components_accordion.html')
def components_badges(request):
    return render(request,'admin_app/components_badges.html')
def components_breadcrumbs(request):
    return render(request,'admin_app/components_breadcrumbs.html')
def components_buttons(request):
    return render(request,'admin_app/components_buttons.html')
def components_cards(request):
    return render(request,'admin_app/components_cards.html')
def components_carousel(request):
    return render(request,'admin_app/components_carousel.html')
def components_list_group(request):
    return render(request,'admin_app/components_list_group.html')
def components_modal(request):
    return render(request,'admin_app/components_modal.html')
def components_pagination(request):
    return render(request,'admin_app/components_pagination.html')
def components_progress(request):
    return render(request,'admin_app/components_progress.html')
def components_spinners(request):
    return render(request,'admin_app/components_spinners.html')
def components_tabs(request):
    return render(request,'admin_app/components_tabs.html')
def components_tooltips(request):
    return render(request,'admin_app/components_tooltips.html')
    
#=========================================================================================#
# :: FORMS ::
def forms_editors(request):
    return render(request,'admin_app/forms_editors.html')
def forms_elements(request):
    return render(request,'admin_app/forms_elements.html')
def forms_layouts(request):
    return render(request,'admin_app/forms_layouts.html')
def forms_validation(request):
    return render(request,'admin_app/forms_validation.html')

#=========================================================================================#
# :: TABLES ::
def tables_data(request):
    return render(request,'admin_app/tables_data.html')
def tables_general(request):
    return render(request,'admin_app/tables_general.html')

#=========================================================================================#
# :: CHARTS ::
def charts_chartjs(request):
    return render(request,'admin_app/charts_chartjs.html')
def charts_apexcharts(request):
    return render(request,'admin_app/charts_apexcharts.html')
def charts_echarts(request):
    return render(request,'admin_app/charts_echarts.html')

#=========================================================================================#
# :: ICONS ::
def icons_bootstrap(request):
    return render(request,'admin_app/icons_bootstrap.html')
def icons_boxicons(request):
    return render(request,'admin_app/icons_boxicons.html')
def icons_remix(request):
    return render(request,'admin_app/icons_remix.html')

#=========================================================================================#
# :: PAGES ::
def users_profile(request):
    user = request.user
    context = {'user': user}
    return render(request,'admin_app/users_profile.html', context)
def pages_faq(request):
    return render(request,'admin_app/pages_faq.html')
def pages_contact(request):
    return render(request,'admin_app/pages_contact.html')
def pages_error_fzf(request):
    return render(request,'admin_app/pages_error_fzf.html')
def pages_blank(request):
    return render(request,'admin_app/pages_blank.html')

#=========================================================================================#
# :: COMMENTS ::
def comments_list_view(request):
    comments = models.comments.objects.all()
    context = {'comments':comments}
    return render(request,'admin_app/list_comments.html',context)

# :: CONTECT ::
def contect_list_view(request):
    contect = models.contect.objects.all()
    context = {'contect':contect}
    return render(request,'admin_app/list_contect.html',context)

# :: SUBSCRIBE ::
def subscribe_list_view(request):
    subscribe = models.subscribe.objects.all()
    context = {'subscribe':subscribe}
    return render(request,'admin_app/list_subscribe.html',context)

#=========================================================================================#
# :: CATEGORY ::
def add_category_view(request):
    if request.method == 'POST':
        form = forms.categorydata(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_app:list_category_view')
        else:
            print(form.errors)
    return render(request,'admin_app/add_category.html')

def list_category_view(request):
    category = models.category.objects.all()
    context = {'category':category}
    return render(request,'admin_app/list_category.html',context)

def update_category_view(request,id):
    up = models.category.objects.get(id=id)
    if request.method == 'POST':
        form = forms.categorydata(request.POST,instance=up)
        if form.is_valid():
            form.save()
            return redirect('admin_app:list_category_view')
        else:
            print(form.errors)
    context = {'up':up}
    return render(request,'admin_app/update_category.html',context)

def delete_category_view(request,id):
    de = models.category.objects.get(id=id)
    de.delete()
    return redirect('admin_app:list_category_view')

#=========================================================================================#
# :: PRODUCT ::
def add_product_view(request):
    cat = models.category.objects.all()
    if request.method == 'POST':
        form = forms.productdata(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()

            # ✅ SAVE MULTIPLE IMAGES
            images = request.FILES.getlist('images')
            for img in images:models.productimage.objects.create(product=product, image=img)

            return redirect('admin_app:list_product_view')
        else:
            print(form.errors)
    context = {'cat':cat}
    return render(request,'admin_app/add_product.html',context)

def list_product_view(request):
    product = models.product.objects.all()
    context = {'product':product}
    return render(request,'admin_app/list_product.html',context)

def update_product_view(request,id):
    cat = models.category.objects.all()
    up = models.product.objects.get(id=id)
    if request.method == 'POST':
        form = forms.productdata(request.POST, request.FILES, instance=up)
        if form.is_valid():
            product = form.save()

            images = request.FILES.getlist('images')
            for img in images:models.productimage.objects.create(product=product, image=img)

            return redirect('admin_app:list_product_view')
        else:
            print(form.errors)
    context = {'up':up, 'cat':cat}
    return render(request,'admin_app/update_product.html',context)

def delete_product_view(request,id):
    de = models.product.objects.get(id=id)
    de.delete()
    return redirect('admin_app:list_product_view')

#=========================================================================================#
# :: USERS ::
def user_list_view(request):
    users = User.objects.all().order_by('-id')
    context = {'users':users}
    return render(request,'admin_app/list_users.html',context)

#=========================================================================================#
# :: BLOCK & UNBLOCK ::
def block_user_view(request,id):
    user = get_object_or_404(User, id=id)
    user.userstatus.is_blocked = True
    user.userstatus.save()
    return redirect('admin_app:user_list_view')

def unblock_user_view(request,id):
    user = get_object_or_404(User,id=id)
    user.userstatus.is_blocked = False
    user.userstatus.save()
    return redirect('admin_app:user_list_view')

#=========================================================================================#
# :: ORDERS & PAYMENTS ::
def order_list_view(request):
    orders = models.Order.objects.all().order_by('-id')
    context = {'orders': orders}
    return render(request, 'admin_app/list_orders.html', context)

def order_detail_view(request, id):
    order = get_object_or_404(models.Order, id=id)
    payment = models.Payment.objects.filter(order=order).first()
    context = {
        'order': order,
        'payment': payment
    }
    return render(request, 'admin_app/order_detail.html', context)

def payment_list_view(request):
    payments = models.Payment.objects.all().order_by('-id')
    context = {'payments': payments}
    return render(request, 'admin_app/list_payments.html', context)

def update_order_status(request, id):
    if request.method == 'POST':
        order = get_object_or_404(models.Order, id=id)
        status = request.POST.get('status')
        order.status = status
        order.save()
        
        # Auto-mark payment as Success if order is Delivered
        if status == 'Delivered':
            payment = models.Payment.objects.filter(order=order).first()
            if payment and payment.payment_status != 'Success':
                payment.payment_status = 'Success'
                payment.save()
                models.Notification.objects.create(message=f"Order #{order.id} delivered. Payment auto-marked as Success.")
        
        # Create notification
        models.Notification.objects.create(message=f"Order #{order.id} status updated to {status}")
        
        return redirect('admin_app:order_detail_view', id=id)

def quick_update_payment_status(request, id):
    payment = get_object_or_404(models.Payment, id=id)
    if request.method == 'POST':
        new_status = request.POST.get('payment_status')
        if new_status in ['Success', 'Pending', 'Failed']:
            payment.payment_status = new_status
            payment.save()
            
            # Auto-align order status
            order = payment.order
            if new_status == 'Success':
                if order.status in ['Pending', 'Cancelled']:
                    order.status = 'Processing'
                    order.save()
                models.Notification.objects.create(message=f"Payment for Order #{order.id} marked as Success")
            elif new_status == 'Failed':
                order.status = 'Cancelled'
                order.save()
                models.Notification.objects.create(message=f"Payment for Order #{order.id} marked as Failed")
            
            messages.success(request, f"Payment status for Order #{order.id} updated to {new_status}")
        else:
            messages.error(request, "Invalid payment status selected.")
    return redirect(request.META.get('HTTP_REFERER', 'admin_app:index'))

#=========================================================================================#
# :: REVIEWS ::
def review_list_view(request):
    reviews = models.ProductReview.objects.all().order_by('-id')
    context = {'reviews': reviews}
    return render(request, 'admin_app/list_reviews.html', context)

def delete_review_view(request, id):
    review = get_object_or_404(models.ProductReview, id=id)
    review.delete()
    return redirect('admin_app:review_list_view')

#=========================================================================================#
# :: NOTIFICATIONS ::
def notification_list_view(request):
    notifications = models.Notification.objects.all().order_by('-id')
    context = {'notifications': notifications}
    return render(request, 'admin_app/list_notifications.html', context)

def mark_notification_read(request, id):
    notification = get_object_or_404(models.Notification, id=id)
    notification.is_read = True
    notification.save()
    return redirect('admin_app:index')
