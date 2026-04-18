from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/create/', views.create_account, name='create_account'),
    path('admin/delete/<int:user_id>/', views.delete_account, name='delete_account'),
    path('admin/toggle/<int:user_id>/', views.toggle_active, name='toggle_active'),
]
