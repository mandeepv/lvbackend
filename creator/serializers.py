from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Campaign, UserCampaign



UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'password', 'first_name', 'last_name', 'city', 'phone_number', 'insta_id', 'youtube_id', 'twitter_id')
        extra_kwargs = {'password': {'write_only': True}}

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'

class UserCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCampaign
        fields = '__all__'
