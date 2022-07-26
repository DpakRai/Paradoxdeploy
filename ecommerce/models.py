import random
import string
from django.db import models

from users.models import UserProfile

class Product(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    active = models.BooleanField(default=True)
    user = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return "Cart id: %s" %(self.id)

    def add_to_cart(self, product_id):
        product = Product.objects.get(pk=product_id)
        new_item, created = CartItem.objects.get_or_create(cart=self, product=product)
        if created:
            print("CartItem Created")
        if new_item.quantity > 0:
            new_item.quantity += 1
            new_item.save()
        return new_item

    def remove_from_cart(self, product_id):
        # Remove a product from the cart
        product = Product.objects.get(pk=product_id)
        cart_item = CartItem.objects.get(cart=self, product=product)
        cart_item.delete()

    def change_qty(self, qty, item_id):
        # Change the quantity of a product in the cart
        cart_item = CartItem.objects.get(pk=item_id)
        cart_item.quantity = qty
        cart_item.save()
    
    def create_order(self):
        # Create an order based on the cart
        order = Order.objects.create(cart=self)
        return order

    @property
    def total_price(self):
        # Calculate the total price of the cart
        return sum([item.product.price*item.quantity for item in self.cartitem_set.all()])

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "%s, %s" %(self.cart.id, self.product.name)

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    canceled = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        '''On save randomly generate non existing transaction id'''
        while self.transaction_id is None or Order.objects.filter(transaction_id=self.transaction_id).exists():
            self.transaction_id = ''.join(
                [
                    random.choice(string.ascii_letters + string.digits) for i in range(0, 50)
                ]
            )
        super().save(*args, **kwargs)


    def __str__(self):
        return "Order id: %s" %(self.id)

    @property
    # Get all cart items related to the order
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        return orderitems

    @property
    # Get the total price of the order
    def get_cart_total(self):
        return self.cart.total_price