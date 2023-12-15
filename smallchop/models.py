from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse





class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name="customer")
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile1.png",  upload_to="profile_pics/", null=True, blank=True)
    date_created =models.DateTimeField(auto_now_add=True, null=True)

    
    @property
    def picURL(self):
        try:
            url = self.profile_pic.url
        except:
            url = ''
        return url 

   

    def __str__(self):
        return str(self.user)
    
   

class Category(models.Model):
    name = models.CharField(max_length=200, null=True )
   
    def __str__(self):
        return self.name

    


class Product(models.Model):
    
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=200, null=True)
    reviews = models.ManyToManyField('smallchop.Review', blank=True, related_name="product_reviews")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    category = models.ManyToManyField(Category, related_name='products')
    image = models.ImageField( upload_to="images/products", null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url  
    
    # def average_rating(self):
    #     reviews = self.review_set.all()
    #     if reviews:
    #         total_ratings = sum(review.rating for review in reviews)
    #         return total_ratings / len(reviews)
    #     return 0
    
class EvtProduct(models.Model):
    
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(max_length=500, null=True, blank=True)
    evtimage = models.ImageField( upload_to="images/products", null=True, blank=True)

    def __str__(self):
        return self.name if self.name else ''
    
    @property
    def imageURL(self):
        try:
            url = self.evtimage.url
        except:
            url = ''
        return url      


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.IntegerField()  # You can use a scale like 1-5 for ratings.
    content = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer} for {self.product}"
    
class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Link the wishlist to a user
    products = models.ManyToManyField(Product, blank=True, related_name="wishlists")

    def __str__(self):
        return f"Wishlist of {self.user.username}"

class Delivery(models.Model):
    customer = models.ForeignKey(Customer,null=True, on_delete=models.SET_NULL)
    location = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.location       

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    delivery = models.ForeignKey(Delivery, null=True, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return str(self.id)

   
       
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])

        

        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    customize = models.ImageField(null=True, blank=True)
    customer_mind = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.product) 

    @property
    def get_total(self):
        total = self.product.price * self. quantity
        return total




class ShippingAddress(models.Model):
    customer =  models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order =  models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    phone1 = models.CharField(max_length=200, null=True)
    phone2 = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True) 


    def __str__(self):
        return self.address 

    

class Event(models.Model):

    TIME_CHOICES = [
        ('AM', 'AM'),
        ('PM', 'PM'),
    ]
    customer =  models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField(max_length=500)
    date = models.DateField()
    time = models.TimeField()
    time_type = models.CharField(max_length=200, choices=TIME_CHOICES, default='AM')
    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15)
    payment_status = models.CharField(max_length=20, default='pending')  # 'pending', 'success', 'failed', etc.
    transaction_id = models.CharField(max_length=50, null=True)
    evtproducts = models.ManyToManyField(EvtProduct, through='EventItem', related_name='event_item')

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Event"

class EventItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    chops = models.ForeignKey(EvtProduct, on_delete=models.CASCADE)
    guest = models.PositiveIntegerField()

   

   
 
class MediaItem(models.Model): 
    file = models.FileField(upload_to='gallery_media/')  # Upload images and videos to a directory

    def __str__(self):
        return self.file
    


class Comment(models.Model):
    customer =  models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.name} - {self.timestamp}'   
    
