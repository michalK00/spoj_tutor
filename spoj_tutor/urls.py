"""
URL configuration for spoj_tutor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from accounts import views as account_views
from admin_extension import views as admin_views

urlpatterns = [
    path("tasks/", include("tasks.urls")),
    path("signup/", account_views.signup, name="signup"),
    path("admin/", include("admin_extension.urls")),


]

handler404 = "tasks.views.page_not_found"
