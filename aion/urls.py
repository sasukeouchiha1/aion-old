"""aion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

# Use include() to add URLS from the application 
from django.conf.urls import include

urlpatterns += [
    url(r'^labreserve/', include('labreserve.urls')),
]

# Add Django site authentication urls (for login, logout, password management)
from django.contrib.auth import views as auth_views

urlpatterns += [
    # The redirect here sends users back to home if they're already logged in
    # https://stackoverflow.com/questions/2320581/django-redirect-logged-in-users-from-login-page
    url(r'^accounts/',
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView

urlpatterns += [
    url(r'^$', RedirectView.as_view(url='/labreserve/', permanent=True)),
]

# Social Auth Google Verification
from django.views.generic.base import TemplateView
urlpatterns += [
    url(r'^google8ee263e74869302f.html', TemplateView.as_view(template_name='google8ee263e74869302f.html'), name="google8ee263e74869302f"),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += [
    url(r'^account/', include('social_django.urls', namespace='social')),
    url(r'^account/', include('django.contrib.auth.urls', namespace='auth')),
]



