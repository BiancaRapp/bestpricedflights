from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Submit
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm

from bestpricedflights.apps.core.models import City
from bestpricedflights.apps.user.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (*UserCreationForm.Meta.fields, "email", "preferred_origin_city")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["preferred_origin_city"].queryset = City.objects.filter(is_origin=True)

        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Sign Up"))


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            *self.fields,
            FormActions(
                Submit("login", "Log In"),
            ),
            HTML('<p>No account yet? <a href="{% url "signup" %}">Sign Up</a></p>'),
            HTML('<p>Forgot your password? <a href="{% url "password_reset" %}">Reset Password</a></p>'),
        )


class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "preferred_origin_city")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["preferred_origin_city"].queryset = City.objects.filter(is_origin=True)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            *self.fields,
            HTML('<p><a href="{% url "password_change" %}">Change Password</a></p>'),
            FormActions(
                Submit("update", "Update"),
            ),
        )
