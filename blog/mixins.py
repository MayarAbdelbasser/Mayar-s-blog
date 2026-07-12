import requests

from django.conf import settings
from django.contrib.auth.mixins import AccessMixin
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.http import HttpResponseRedirect
from django.urls import reverse
from blog.models import Author


class JWTRequiredMixin(AccessMixin):
    # login_url = reverse("signin")

    def dispatch(self, request, *args, **kwargs):
        access = request.session.get("access_token")
        refresh = request.session.get("refresh_token")

        if not access or not refresh:
            # return self.handle_no_permission()
            return HttpResponseRedirect(reverse("signin"))

        try:
            # Validate access token
            token = AccessToken(access)
            request.user = Author.objects.get(id=token["user_id"])

        except TokenError:
            # Access expired -> refresh it
            response = requests.post(
                f"{settings.API_BASE_URL}/api/token/refresh/",
                json={"refresh": refresh},
                timeout=10,
            )

            if response.status_code != 200:
                request.session.flush()
                # return self.handle_no_permission()
                return HttpResponseRedirect(reverse("signin"))

            data = response.json()

            # Save new tokens
            request.session["access_token"] = data["access"]

            if "refresh" in data:
                request.session["refresh_token"] = data["refresh"]

            # Authenticate again
            token = AccessToken(data["access"])
            request.user = Author.objects.get(id=token["user_id"])

        return super().dispatch(request, *args, **kwargs)
