from django.conf import settings
import jwt
from datetime import datetime, timedelta
from rest_framework.authentication import BaseAuthentication

from .models import JWT, MyUsers




def get_access_token(payload, to_expire: int = 360):
    return jwt.encode(
        {"exp": datetime.now() + timedelta(minutes=6000), **payload},
        settings.SECRET_KEY,
        algorithm='HS256'
    )




class MyAuthentication(BaseAuthentication):

    def authenticate(self, request):
        data = self.validate_request(request.headers)
        if not data:
            return None, None

        return self.get_user(data['user_id']), None

        
        
    def get_user(self, user_id):
        try:
            user = MyUsers.objects.get(id=user_id)
            return user
        except Exception:
            return None



    def validate_request(self, headers):
        authorization = headers.get('Authorization', None)
        if not authorization:
            return None
        token = headers['Authorization'].split(' ')[-1]
        decoded_data = self.verify_token(token)

        try:
            user_jwt = JWT.objects.get(user=decoded_data['user_id'])
        except JWT.DoesNotExist:
            return None

        if user_jwt.access != token:
            return None

        if not decoded_data:
            return None

        return decoded_data


    @staticmethod
    def verify_token(token):
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except Exception:
            return None

        exp = decoded['exp']

        # if datetime.now().timestamp() > exp:
        #     return None
        
        
        return decoded