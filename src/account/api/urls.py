from django.urls import path
from account.api.views import (
    registration_view,
    GetAuthTokenView,
)


app_name = 'account'

urlpatterns = [
    path('login', GetAuthTokenView.as_view(), name="login"),
    path('register', registration_view, name="register"),
]
