from django.urls import path

from .views import GetToken, RegistrationView

app_name = 'core'

urlpatterns = (
    path('get-token/', GetToken.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
)
