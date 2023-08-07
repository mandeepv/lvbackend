from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    username = None
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be entered in the format: '9999999999'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True) 
    insta_id = models.CharField(max_length=100, blank=True)
    youtube_id = models.CharField(max_length=100, blank=True)
    twitter_id = models.CharField(max_length=100, blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'city']
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not (self.insta_id or self.youtube_id or self.twitter_id):
            raise ValueError("At least one of Insta ID, YouTube ID, or Twitter ID must be provided.")
        super(User, self).save(*args, **kwargs)


class Campaign(models.Model):
    campaign_id = models.AutoField(primary_key=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    campaign_info = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)


class UserCampaign(models.Model):
    class CampaignState(models.TextChoices):
        APPLIED = 'Applied', ('Applied')
        SELECTED = 'Selected', ('Selected')
        UNDER_REVIEW = 'Under Review', ('Under Review')
        APPROVED = 'Approved', ('Approved')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=15,
        choices=CampaignState.choices,
        default=CampaignState.APPLIED,
    )

    class Meta:
        unique_together = ('user', 'campaign')
