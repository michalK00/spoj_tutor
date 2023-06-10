from django.urls import path
from django.contrib.auth import views
from .views import signup

urlpatterns = [
    # TODO: add tests for logout, login, signup, password change
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('login', views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('signup', signup, name="signup"),
    path('password', views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name="password_change"),
    path('password/done/', views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name="password_change_done"),
]

handler404 = "tasks.views.page_not_found"
