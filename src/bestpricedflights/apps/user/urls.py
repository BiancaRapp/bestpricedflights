from django.contrib.auth.views import LoginView
from django.urls import include, path

from .forms import CustomAuthenticationForm

urlpatterns = [
    path("login/", LoginView.as_view(form_class=CustomAuthenticationForm), name="login"),
    path("", include("django.contrib.auth.urls")),
]
