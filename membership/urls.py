from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='membership_home'),
    # path('status/', views.payment_status, name='status'),

]
