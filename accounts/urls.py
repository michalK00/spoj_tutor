from django.urls import path
from django.contrib.auth import views
from .views import signup, login_view

urlpatterns = [
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('login', views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('signup', signup, name="signup"),
]

handler404 = "tasks.views.page_not_found"
