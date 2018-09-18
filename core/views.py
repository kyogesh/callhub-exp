from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import UserSerializer

app_label = 'core'

User = get_user_model()


class GetToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(GetToken, self).post(request, *args, **kwargs)
        user = User.objects.get(auth_token__key=response.data.get('token'))
        user_logged_in.send(sender=User, request=request, user=user)
        return response


class RegistrationView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'token': user.auth_token.key, 'username': user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
