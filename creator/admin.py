
# Register your models here.
from django.contrib import admin
from .models import User, Campaign, UserCampaign

admin.site.register(User)
admin.site.register(Campaign)
admin.site.register(UserCampaign)
