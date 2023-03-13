
import datetime

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from PIL import Image


def image_validator(image):
    megabyte_limit = 2.0
    if image.file.size > megabyte_limit * 1024 * 1024:
        raise ValidationError("Image is too big")
    width, height = Image.open(image).size
    if width > 2880 or height > 1440:
        raise ValidationError("Image is too big")


# removed because Django is probably unable to serialize local functions and lambdas
# def maximum_size(max_width, max_height):
#     def validator(image):
#         width, height = Image.open(image).size
#         print(width, height)
#         if width > max_width or height > max_height:
#             raise ValidationError("Image is too big")
#     return validator


class EventStatus(models.TextChoices):
    Open = "Open"
    Closed = "Closed"
    Completed = "Completed"
    Archived = "Archived"


class EventType(models.TextChoices):
    Virtual = "Virtual"
    Physical = "Physical"


class Marketplace(models.Model):
    Creator = models.ForeignKey(User, on_delete=models.CASCADE)
    Image_URL = models.ImageField(
        null=False, blank=True, upload_to='event_images', default='images/Logo_Colour.png',
        validators=[image_validator]
        )
    Speaking_Event_Name = models.CharField(max_length=100)
    Type = models.CharField(max_length=9, choices=EventType.choices, default=EventType.Virtual)
    Location = models.CharField(max_length=500, null=True)
    Capacity = models.PositiveIntegerField(
        default=10, validators=[MinValueValidator(1), MaxValueValidator(30000)])
    Topic = models.CharField(max_length=40) #Todo change tp 40 !!!!!!!!
    Worth = models.PositiveIntegerField(
     validators=[MinValueValidator(1), MaxValueValidator(50000)])
    date = models.DateTimeField(default=timezone.now)
    Description = models.CharField(max_length=5000)
    Status = models.CharField(max_length=9, choices=EventStatus.choices, default=EventStatus.Open)

    def __str__(self):
        return self.Speaking_Event_Name

    def status(self):
        return EventStatus.Completed if timezone.now() > self.date else self.Status


class speaker_applied_event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Marketplace, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.event_id

class JobPostStatus(models.TextChoices):
    Open = "Open"
    Closed = "Closed"

class JobMode(models.TextChoices):
    Part_time = "Part time"
    Full_time = "Full time"
    Contract = "Contract"
    Permanent = "Permanent"

class Job_post(models.Model):
    Creator = models.ForeignKey(User, on_delete=models.CASCADE)
    Image_URL = models.ImageField(
        null=False, blank=True, upload_to='job_images', default='images/Logo_Colour.png',
        validators=[image_validator]
        )
    Email = models.EmailField(max_length=254)
    Job_role = models.CharField(max_length=100)
    Company = models.CharField(max_length=100)
    Job_mode = models.CharField(max_length=20, choices=JobMode.choices, default=JobMode.Full_time)
    Status = models.CharField(max_length=20, choices=JobPostStatus.choices, default=JobPostStatus.Open)
    Deadline = models.DateTimeField(default=timezone.now)
    Salary = models.PositiveBigIntegerField(validators=[MinValueValidator(1), MaxValueValidator(500000)])
    Description = models.CharField(max_length=5000)

    def __str__(self):
        return self.Job_role + " at " + self.Company

    def status(self):
        return JobPostStatus.Closed if timezone.now() > self.Deadline else self.Status

class seeker_applied_job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_position = models.ForeignKey(Job_post, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.job_id

def image_location(self, filename):
    return 'cover_images/{}/{}'.format(self.slug, filename)


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextUploadingField(config_name='default', null=True, blank=True)
    post_date = models.DateField(auto_now_add=True)
    cover_image = models.ImageField(upload_to=image_location, null=True, blank=True)
    slug = models.SlugField(max_length=200, db_index=True, null=True, blank=True, unique=True)
    mailed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"post_slug": self.slug})


#create a table for the events topics
class Events_topic(models.Model):
    topic = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.topic

class TeamMember(models.Model):
    fullName = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    image_url = models.ImageField(null=False, blank=True, upload_to='headshots', default='headshots/placeholder.jpeg')

    def __str__(self):
        return self.fullName

class Opportunity_suggestion(models.Model):
    opportunity = models.CharField(max_length=50, null=True, unique=True)
    count = models.IntegerField(default=1)

    def __str__(self):
        return self.opportunity

class Opportunity_suggestion_user_data(models.Model):
    user_id = models.CharField(max_length=10, null=True, blank=True)
    firstname = models.CharField(max_length=60, null=True, blank=True)
    email = models.CharField(max_length=60, null=True, blank=True)
    telephone = models.CharField(max_length=60, null=True, blank=True)
    opportunity = models.CharField(max_length=60, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=60, null=True, blank=True)
    desired_region = models.CharField(max_length=60, null=True, blank=True)
    countrycode = models.CharField(max_length=4, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)

class Newsletter_email(models.Model):
    email = models.CharField(max_length=50, null=True, unique=True)

    def __str__(self):
        return self.email

class Opportunity_Portfolio_mailing_list(models.Model):
    email = models.CharField(max_length=50, null=True, unique=True)
    name = models.CharField(max_length=100, null=True)
    company = models.CharField(max_length=50, null=True, default="None")

    def __str__(self):
        return self.email



class Opportunity_Verified_mailing_list(models.Model):
    opp_portfolio_email = models.ForeignKey(Opportunity_Portfolio_mailing_list, on_delete=models.CASCADE)

    def __str__(self):
        return self.opp_portfolio_email
