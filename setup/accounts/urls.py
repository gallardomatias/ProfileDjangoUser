from django.urls import path
from .views import main,UserProfileView

app_name= "accounts"

urlpatterns = [
    path('', main, name='main'),
    path('users/<username>/',UserProfileView.as_view(), name='UserProfileView'),
]