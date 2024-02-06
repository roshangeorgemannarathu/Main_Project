from django.contrib.auth.models import Group
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class dealer(AbstractUser):
    email = models.EmailField(unique=True)
    fullname = models.TextField(max_length=100, default="")
    role = models.TextField(max_length=100, default="")
    
    def __str___(self):
        return self.username
    
class UserProfile(models.Model):
    user = models.ForeignKey("Dealer", on_delete=models.CASCADE)  # Assuming you have a ForeignKey relationship with the Dealer model
    fullname = models.CharField(max_length=100)
    dateofbirth = models.DateField()
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

    def __str__(self):
        return f"{self.user.user.username}'s Cart Item - {self.item_category} {self.item_id}"



    


   