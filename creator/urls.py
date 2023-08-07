from django.urls import path
from .views import SignUpView, SignInView, CampaignListCreateView, UserCampaignListCreateView, UpdateUserCampaignState
from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('campaign/', CampaignListCreateView.as_view(), name='campaign'),
    path('usercampaigns/', UserCampaignListCreateView.as_view(), name='usercampaigns'),
    path('usercampaigns/update_state/user/<int:user_id>/campaign/<int:campaign_id>/', UpdateUserCampaignState.as_view(), name='update-usercampaign-state'),

    
]
from django.urls import path
