from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    has_water = models.BooleanField(default=False, null=True, blank=True)
    has_electricity = models.BooleanField(default=False,  null=True, blank=True)
    phone_number = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)         # fixé automatiquement à la création
    custom_date = models.DateTimeField(default=timezone.now) 
    LISTING_TYPE_CHOICES = [
        ('sale', 'À vendre'),
        ('rent', 'À louer'),
    ]
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, default='sale')
    property_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, default='rent')
    likes = models.ManyToManyField(User, related_name='liked_properties', blank=True)
    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title
    
class PropertyImage(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')

    def __str__(self):
        return f"Image for {self.property.title}"
    
class Comment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.user} on {self.property}" 

class Like(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('property', 'user')  # un seul like par user


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, default=True)
    is_email_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # Sauvegarder le profil s'il existe (utile si on modifie le user)
        try:
            instance.userprofile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)