"""django_tiny URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as django_views
from webapp import views as webapp_view
from webapp.forms import *


urlpatterns = [
    url(r'^$', 'webapp.views.home'),
    url(r'^home/$', webapp_view.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),

    # url groups
    url(r'^user/', include('webapp.urls_user', namespace='user')),
    url(r'^registration/', include('webapp.urls_auth', namespace='auth')),
    url(r'^staff/', include('webapp.urls_staff', namespace='staff')),

    url(r'^password_reset/$', django_views.password_reset,
        {'template_name': 'webapp/registration/password_reset_form.html',
         'email_template_name': 'webapp/registration/password_reset_email.html',
         'password_reset_form': PasswordResetForm},
        name='password_reset'),
]
