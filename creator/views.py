from django.contrib.auth import get_user_model, authenticate
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token

from rest_framework import generics
from .models import Campaign
from .serializers import CampaignSerializer
from .models import UserCampaign
from .serializers import UserCampaignSerializer



from rest_framework.views import APIView


UserModel = get_user_model()

class SignUpView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = UserModel.objects.create_user(**serializer.validated_data)
            return Response({"user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(views.APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.user_id,  # include user_id in the response
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "city": user.city,
                "phone_number": user.phone_number,
                "insta_id": user.insta_id,
                "youtube_id": user.youtube_id,
                "twitter_id": user.twitter_id
            })
        else:
            return Response({
                "error": "Wrong email or password"
            }, status=status.HTTP_400_BAD_REQUEST)
        


# View for handling GET and POST requests to /creator/usercampaigns/
class UserCampaignListCreateView(generics.ListCreateAPIView):
    queryset = UserCampaign.objects.all()
    serializer_class = UserCampaignSerializer


# View for handling GET and POST requests to /creator/campaigns/
class CampaignListCreateView(generics.ListCreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


class UpdateUserCampaignState(APIView):

    def patch(self, request, user_id, campaign_id):
        try:
            user_campaign = UserCampaign.objects.get(user_id=user_id, campaign_id=campaign_id)
            new_state = request.data.get("state")

            if new_state not in ["Applied", "Selected", "Under Review", "Approved"]:
                return Response({"error": "Invalid state provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            user_campaign.state = new_state
            user_campaign.save()

            return Response({"message": f"State updated to {new_state}"}, status=status.HTTP_200_OK)

        except UserCampaign.DoesNotExist:
            return Response({"error": "UserCampaign entry not found"}, status=status.HTTP_404_NOT_FOUND)
