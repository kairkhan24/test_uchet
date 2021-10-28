import jwt
from datetime import datetime, timedelta
from rest_framework.views import APIView, Response
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

from .models import CustomUser


class LoginView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = CustomUser.objects.filter(email=email).first()

        if not user:
            raise AuthenticationFailed(f'User with email {email} does not exists.')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        exp = datetime.utcnow() + timedelta(hours=2)
        iat = datetime.utcnow()

        payload = {
            'id': user.id,
            'exp': exp,
            'iat': iat,
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}
        return response


class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'info': 'success'}
        return response
