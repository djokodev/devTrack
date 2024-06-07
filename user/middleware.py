from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.deprecation import MiddlewareMixin

class RefreshJWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            authorization_header = request.META['HTTP_AUTHORIZATION']
            auth_parts = authorization_header.split(' ')
            if len(auth_parts) == 2 and auth_parts[0] == 'Bearer':
                access_token = auth_parts[1]
                decoded_token = RefreshToken(access_token, verify=False)
                if decoded_token and hasattr(decoded_token, 'token') and 'exp' in decoded_token.token:
                    if decoded_token.token['exp'] < datetime.utcnow() + timedelta(minutes=5):
                        refresh = decoded_token.refresh()
                        request.META['HTTP_AUTHORIZATION'] = f'Bearer {refresh.access_token}'

