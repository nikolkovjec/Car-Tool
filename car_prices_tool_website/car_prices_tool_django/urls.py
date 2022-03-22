"""car_prices_tool_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import api
from api import urls
from django.contrib import admin
from django.contrib.auth import views as django_auth_views
from django.urls import path, include
from car_prices_tool.views import auth_views, price_tools_views, templates_views, users_views


urlpatterns = [
    # Admin:
    path('admin/', admin.site.urls, name='admin'),

    # Templates:
    path('', templates_views.home, name='home'),
    path('about/', templates_views.about, name='about'),
    path('features/', templates_views.features, name='features'),
    path('pricing/', templates_views.pricing, name='pricing'),
    path('search/', price_tools_views.search, name='search'),
    path('results/', price_tools_views.results, name='results'),
    path('results_demo/', price_tools_views.results_demo, name='results_demo'),
    path('no_results/', price_tools_views.no_results, name='no_results'),
    path('go_premium/', users_views.go_premium, name='go_premium'),
    path('go_api_pro/', users_views.go_api_pro, name='go_api_pro'),
    path('api_documentation/', templates_views.api_documentation, name='api_documentation'),

    # Authorization:
    path('signup/', auth_views.SignUpView.as_view(), name='signup'),
    path('login/', django_auth_views.LoginView.as_view(), name='login'),
    path('logout/', django_auth_views.LogoutView.as_view(), name='logout'),

    # API:
    path('api/', include(api.urls)),

    # Ajax:
    path('ajax/load_models/', templates_views.load_models, name='ajax_load_models'),

    # Django Debug Toolbar
    # path(r'^__debug__', include(debug_toolbar.urls))
]
