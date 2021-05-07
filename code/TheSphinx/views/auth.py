import jwt
import json
import requests
import base64

from django.contrib.auth import login, logout

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from TheMeetingSphinx.settings import CONFIG_VARS

from TheSphinx.models.user import User
from TheSphinx.serializers.user import UserGetSerializer, UserPostSerializer


class AuthViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update" or self.action == "partial":
            return UserPostSerializer
        else:
            return UserGetSerializer

    @action(detail=False, methods=['post', ],)
    def login(self, request):
        if request.user.is_authenticated:
            return Response({'Error': 'User is already logged in!', }, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = request.data
            code = data['code']

            token_endpoint = "https://oauth2.googleapis.com/token"

            data = {
                'code': code,
                'client_id': CONFIG_VARS["GOOGLE"]["CLIENT_ID"],
                'client_secret': CONFIG_VARS["GOOGLE"]["CLIENT_SECRET"],
                'redirect_uri': CONFIG_VARS["FRONTEND"]["REDIRECT_URI"],
                'grant_type': 'authorization_code',
            }

            token_response = requests.post(
                url=token_endpoint,
                data=data
            ).json()

            if token_response == None:
                return Response(
                    {'Error': 'Invalid Token'}, status=status.HTTP_401_UNAUTHORIZED
                )

            id_token_jwt = token_response['id_token']

            content = id_token_jwt.split('.')[1]
            padding = len(str(content)) % 4
            content = content + padding*"="

            content_bytes = base64.b64decode(content)
            content_ascii = content_bytes.decode('ascii')
            user_data = json.loads(content_ascii)

            try:
                user = User.objects.get(email=user_data['email'])
                login(request, user)
                user_serializer = UserGetSerializer(user)
                user_data = user_serializer.data
                return Response({
                    'status': 'Successfully logged in',
                    'user': user_data,
                },
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                email = user_data['email']
                full_name = user_data['name']
                if email == 'pragya_d@cs.iitr.ac.in':
                    full_name = "Giteshwari Geetamma"
                username = user_data['given_name']
                profile_picture = user_data['picture']

                new_user = User(
                    email=email,
                    full_name=full_name,
                    username=username,
                    profile_picture=profile_picture,
                )

                new_user.save()
                login(request, new_user)

                new_user_serializer = UserGetSerializer(new_user)
                new_user_data = new_user_serializer.data
                return Response({
                    'status': 'Successfully logged in',
                    'user': new_user_data,
                },
                    status=status.HTTP_200_OK
                )

    @action(detail=False, methods=['post', ],)
    def logout(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({
                'status': 'Successfully logged out',
            })
        else:
            return Response({'Error': 'User is not logged in', }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', ],)
    def verify(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            serializer = self.get_serializer_class()(user)
            response_data = {
                'login_status': True,
                'user': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'login_status': False, },)
