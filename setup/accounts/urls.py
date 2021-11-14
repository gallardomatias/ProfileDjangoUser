from django.urls import path, include
from rest_framework import routers
from .views import main,UserProfileView

from accounts import views


from rest_framework.routers import DefaultRouter


app_name= "accounts"


router= DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('user', views.UserViewSet, basename='user')

urlpatterns = [
    path('', main, name='main'),
    path('users/<username>/',UserProfileView.as_view(), name='UserProfileView'),
    path('api/hello-view/',views.HelloApiView.as_view()),
    path('api/', include(router.urls)),
    path('login/', views.UserLoginApiView.as_view()),
]