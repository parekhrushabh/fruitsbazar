from django.db import models
from django.contrib.auth.models import User

# ===================== MODELS ===================== #

class comments(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

class contect(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.IntegerField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

class subscribe(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

class category(models.Model):
    name = models.CharField(max_length=255)

# class subcategory(models.Model):
#     category = models.ForeignKey(category, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)

class product(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    # subcategory = models.ForeignKey(subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.PositiveIntegerField(help_text="Stock available")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Item_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(
        max_length=50,
        choices=[
            ('kg', 'Kilogram'),
            ('g', 'Gram'),
            ('pcs', 'Pieces'),
            ('dozen', 'Dozen')
        ]
    )

class productimage(models.Model):
    product = models.ForeignKey(product,related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/multiple/')

class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

# ===================================================================================================
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_status(sender, instance, created, **kwargs):
    if created:
        UserStatus.objects.create(user=instance)

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.full_name}"

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.price

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='Success')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.transaction_id}"
class ProductReview(models.Model):
    product = models.ForeignKey(product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.product.name} by {self.user.username}'

class Notification(models.Model):
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
