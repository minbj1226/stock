"""joljak URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('', include("dashboard.urls")),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('user_analysis/', include('user_analysis.urls')),
    path('mock_investment/', include('mock_investment.urls')),
    path('recommend/', include('recommend.urls')),
    path('stocks/', include('stocks.urls')),
    path('mypage/', include('mypage.urls')),
]