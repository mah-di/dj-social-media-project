from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.deletion import CASCADE
from django.dispatch.dispatcher import receiver
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, related_name='profile')
    set_pro_pic = models.ImageField(upload_to='profile_pics', blank=True, default='')
    pro_pic = models.CharField(max_length=400)
    countries = (
        ('Afghanistan', 'Afghanistan'),
        ('Bangladesh', 'Bangladesh'),
        ('Egypt', 'Egypt'),
        ('Pakistan', 'Pakistan'),
        ('Turkey', 'Turkey'),
        ('UAE', 'UAE'),
        ('UK', 'UK'),
        ('USA', 'USA'),
        ('Zimbabwe', 'Zimbabwe'),
    )
    country = models.TextField(choices=countries, blank=True, default='')
    dob = models.DateField(blank=True, null=True, verbose_name='Date of Birth')
    phone_number = PhoneNumberField(blank=True)
    facebook_profile = models.URLField(verbose_name='Your Facebook Profile Link', blank=True)
    insta_profile = models.URLField(verbose_name='Your Instagram Profile Link', blank=True)
    bio = models.TextField(verbose_name='Write a short bio..', blank=True, max_length=400)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.set_pro_pic:
            self.pro_pic = self.set_pro_pic
        else:
            self.pro_pic = 'profile_pics/pfp.jpg'

        return super().save(*args, **kwargs)



@receiver(post_save, sender=User)
def user_profile_init(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)