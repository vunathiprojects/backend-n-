from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import AnonymousUser

class NoAuthAuthentication(BaseAuthentication):
    """
    Custom authentication class that ignores all authentication
    and always returns an anonymous user.
    """
    def authenticate(self, request):
        return (AnonymousUser(), None)
