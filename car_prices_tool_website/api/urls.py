from django.urls import path

from . import views

urlpatterns = [
    # CRUD
    path('cars/results', views.CarsResults.as_view(), name='api_results'),
    path('cars/create', views.CarCreate.as_view(), name='api_create'),
    path('cars/<int:pk>', views.CarRetrieveUpdateDestroy.as_view(), name='api_details'),

    # Auth
    path('signupuser', views.sign_up_user, name='api_signupuser'),
    path('gettoken', views.get_token, name='api_gettoken')
]
