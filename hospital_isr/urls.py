from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from .views import set_language_view


def home_redirect(request):
    if request.user.is_authenticated:
        if request.user.is_admin_user():
            return redirect('accounts:admin_dashboard')
        elif request.user.is_doctor() or request.user.is_nurse_user():
            return redirect('doctors:dashboard')
        else:
            return redirect('patients:dashboard')
    return redirect('accounts:login')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),
    path('set-language/', set_language_view, name='set_language'),
    path('accounts/', include('accounts.urls')),
    path('patients/', include('patients.urls')),
    path('doctors/', include('doctors.urls')),
]
