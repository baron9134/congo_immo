from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 


# Type de bien (Maison, Appartement, Terrain...)
class PropertyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Ville
class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Bien immobilier
class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField()
    description = models.TextField()
    main_image = models.ImageField(upload_to='properties/', null=True, blank=True)
    bedrooms = models.IntegerField(default=0)
    living_rooms = models.IntegerField(default=0)
    has_water = models.BooleanField(default=False)
    has_electricity = models.BooleanField(default=False)
    phone_number = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)         # fixé automatiquement à la création
    custom_date = models.DateTimeField(default=timezone.now) 
    def __str__(self):
        return self.title
    
class PropertyImage(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')

def __str__(self):
        return f"Image for {self.property.title}"
