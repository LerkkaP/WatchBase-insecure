from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path('logout', views.logout, name='logout'),
    path('watches', views.watches, name="watches"),
    path('details/<int:id>', views.details, name='details')
]