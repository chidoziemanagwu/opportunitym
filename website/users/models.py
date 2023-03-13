from email.policy import default
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import (FileExtensionValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstTime_user = models.BooleanField(default=True)
    profile_pic_URL = models.ImageField(
        null=True, blank=True, upload_to='speaker_profile_image')
    Job_title = models.CharField(max_length=200, null=True, blank=True)
    Company = models.CharField(max_length=200, null=True, blank=True)
    Phone_number = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    bio_video_URL = models.FileField(upload_to='speaker_profile_video', null=True, blank=True,
                                     validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
                                    

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()

class Stripe_account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=200)

    def __str__(self):
        return self.stripe_id


