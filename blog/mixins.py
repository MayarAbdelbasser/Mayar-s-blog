import requests
from django.conf import settings
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from blog.models import Author


class BaseJWTMixin(AccessMixin):

    def authenticate_jwt(self, request):
        access = request.session.get("access_token", "")
        refresh = request.session.get("refresh_token", "")

        if not access or not refresh:
            return False

        try:
            token = AccessToken(access)
            request.user = Author.objects.get(id=token["user_id"])
            return True

        except TokenError:
            try:
                response = requests.post(
                    f"{settings.API_BASE_URL}/api/token/refresh/",
                    json={"refresh": refresh},
                    timeout=10,
                )
            except requests.RequestException:
                return False

            if response.status_code != 200:
                request.session.flush()
                return False

            data = response.json()

            request.session["access_token"] = data["access"]
            if "refresh" in data:
                request.session["refresh_token"] = data["refresh"]

            token = AccessToken(data["access"])
            request.user = Author.objects.get(id=token["user_id"])
            return True

        except Author.DoesNotExist:
            return False


class JWTRequiredMixin(BaseJWTMixin):

    def dispatch(self, request, *args, **kwargs):
        if not self.authenticate_jwt(request):
            return HttpResponseRedirect(reverse("signin"))

        return super().dispatch(request, *args, **kwargs)


class AuthVerifiedMixin(BaseJWTMixin):
    is_Authenticated = False

    def dispatch(self, request, *args, **kwargs):
        if not self.authenticate_jwt(request):
            self.is_Authenticated = False
        else:
            self.is_Authenticated = True
        return super().dispatch(request, *args, **kwargs)
