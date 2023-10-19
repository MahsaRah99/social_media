from django.urls import path
from users import views

app_name = 'posts'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]