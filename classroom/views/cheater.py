from django.shortcuts import redirect, render
from django.contrib.auth import logout

def cheater_view(request, *args, **kwargs):
    logout(request)
    return render(request, 'registration/logout.html', {})
