from django.contrib.auth.views import LoginView
from django.urls import include, path

from bestpricedflights.apps.user import views

from .forms import CustomAuthenticationForm

urlpatterns = [
    path("login/", LoginView.as_view(form_class=CustomAuthenticationForm), name="login"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("profile/", views.EditProfileView.as_view(), name="edit_profile"),
    path("", include("django.contrib.auth.urls")),
]
