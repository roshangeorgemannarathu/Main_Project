from django.contrib.auth.models import Group
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class dealer(AbstractUser):
    email = models.EmailField(unique=True)
    # is_delivery_man = models.BooleanField(default=False)
    fullname = models.TextField(max_length=100, default="")
    role = models.TextField(max_length=100, default="")

    
    
    def __str___(self):
        return self.username
    
class UserProfile(models.Model):
    user = models.ForeignKey("Dealer", on_delete=models.CASCADE)  # Assuming you have a ForeignKey relationship with the Dealer model
    fullname = models.CharField(max_length=100)
    dateofbirth = models.DateField(null=True)
    phone = models.CharField(max_length=10)
    housename = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    district = models.CharField(max_length=50, choices=[  # Add choices for the available districts
        ("Thiruvananthapuram", "Thiruvananthapuram"),
        ("Kollam", "Kollam"),
        ("Pathanamthitta", "Pathanamthitta"),
        ("Alappuzha", "Alappuzha"),
        ("Kottayam", "Kottayam"),
        ("Idukki", "Idukki"),
        ("Ernakulam", "Ernakulam"),
        ("Thrissur", "Thrissur"),
        ("Palakkad", "Palakkad"),
        ("Malappuram", "Malappuram"),
        ("Kozhikode", "Kozhikode"),
        ("Wayanad", "Wayanad"),
        ("Kannur", "Kannur"),
        ("Kasaragod", "Kasaragod"),
        
        # Add other districts here
         
    ])
    photoid = models.FileField(upload_to='photoids/')  # Make sure to configure your media settings for file uploads
    photo = models.ImageField(upload_to='photos/')  # Make sure to configure your media settings for image uploads

    def __str__(self):
        return self.fullname

class Aquarium(models.Model):
    dealer = models.ForeignKey(dealer, on_delete=models.CASCADE)  # Add this line to create the foreign key relationship
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=30, null=True)
    image = models.ImageField(upload_to='aquarium_images/')

    def __str__(self):
        return self.name

class Pet(models.Model):
    dealer = models.ForeignKey(dealer, on_delete=models.CASCADE)  # Add this line to create the foreign key relationship
    CATEGORY_CHOICES = [
        ('dog', 'Dogs'),
        ('cat', 'Cats'),
        ('fish', 'Fish'),
        ('bird', 'Birds'),
    ]

    category = models.CharField(max_length=4, choices=CATEGORY_CHOICES)
    # sub_category =models.CharField(max_length=10, choices=)
    pet_breed = models.CharField(max_length=100, null=True)
    pet_age = models.CharField(max_length=10 ,null=True)
    
    pet_description = models.TextField(max_length=30, null=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pet_images/')

    def __str__(self):
        return f"{self.get_category_display()} - {self.id}"


class CartItem(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    item_category = models.CharField(max_length=255)  # 'pet' or 'aquarium'
    item_id = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    # Add a foreign key to the respective item model (Pet or Aquarium)
    # You may need to adjust these fields based on your actual models
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True, blank=True)
    aquarium = models.ForeignKey(Aquarium, on_delete=models.CASCADE, null=True, blank=True)



 #payment table
        
class Userpayment(models.Model):
    user      =     models.ForeignKey(dealer, on_delete=models.CASCADE,null=True,blank=True)
    cart = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField(default=0)
    datetime = models.TextField(default="empty")
    order_id_data = models.TextField(default="empty")
    payment_id_data = models.TextField(default="empty")
    item = models.ForeignKey(Pet,on_delete=models.CASCADE, null=False) 
    status = models.TextField(default="active")

    def __str__(self):
        return f"Payment {self.id} - {self.user_profile.fullname}"  # Assuming UserProfile has a 'fullname' field
       

class Userpayment_aquarium(models.Model):
    user      =     models.ForeignKey(dealer, on_delete=models.CASCADE,null=True,blank=True)
    cart = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField(default=0)
    datetime = models.TextField(default="empty")
    order_id_data = models.TextField(default="empty")
    payment_id_data = models.TextField(default="empty")
    item = models.ForeignKey(Aquarium,on_delete=models.CASCADE, null=False) 
    status = models.TextField(default="active") 

    def __str__(self):
        return f"Payment {self.id} - {self.user_profile.fullname}"  # Assuming UserProfile has a 'fullname' field
       

    


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    dealer = models.ForeignKey(dealer, on_delete=models.CASCADE, related_name='reviews')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES,null=True)
    review_text = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.product_name} by {self.dealer.username}'
    

class Review_Aquarium(models.Model):
    RATING_CHOICES_aqu = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    dealer_aqu = models.ForeignKey(dealer, on_delete=models.CASCADE, related_name='aquarium_reviews')
    aquarium = models.ForeignKey(Aquarium, on_delete=models.CASCADE, related_name='reviews')
    rating_aqu = models.IntegerField(choices=RATING_CHOICES_aqu, null=True)
    review_text_aqu = models.TextField(null=True)
    created_at_aqu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.aquarium.name} by {self.dealer.username}'
    

class DeliveryMan(models.Model):
     name = models.CharField(max_length=100)
     email = models.EmailField()
     phone = models.CharField(max_length=15)
     house_name = models.CharField(max_length=100)
     district = models.CharField(max_length=100)
     city = models.CharField(max_length=100)
     pincode = models.CharField(max_length=10)
     vehicle_type = models.CharField(max_length=50)
     vehicle_no = models.CharField(max_length=20)

     def __str__(self):
        return self.name   
     


class SelectedItem(models.Model):
    user = models.ForeignKey(DeliveryMan, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    item = models.CharField(max_length=255)
    status = models.CharField(max_length=100)