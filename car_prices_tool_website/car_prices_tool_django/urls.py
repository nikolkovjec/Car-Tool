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
from django.contrib import admin
from django.urls import path, include
from car_prices_tool import views
import debug_toolbar

urlpatterns = [
    # Admin:
    path('admin/', admin.site.urls),

    # Templates:
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('features', views.features, name='features'),
    path('pricing', views.pricing, name='pricing'),
    path('search', views.search, name='search'),
    path('results', views.results, name='results'),
    path('no_results', views.no_results, name='no_results'),
    path('go_premium', views.go_premium, name='go_premium'),

    # Authorization:
    path('signup', views.sign_up_user, name='signup'),
    path('login', views.log_in_user, name='login'),
    path('logout', views.log_out_user, name='logout'),

    # Ajax:
    path('ajax/load-cities/', views.load_models, name='ajax_load_models'),

    path(r'^__debug__', include(debug_toolbar.urls))
]
