from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.models import User

from .models import Profile

# Create your views here.

def main(request):
    return render(request, 'accounts/main.html', {})

class UserProfileView(View):
    def get(self,request,username,*args,**kwargs):
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(user=user)
        context={
            'user':user,
            'profile':profile
        }
        return render(request,'accounts/main.html',context)