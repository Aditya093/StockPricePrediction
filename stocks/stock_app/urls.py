from django.urls import path
from . import views


urlpatterns=[
    path('',views.Login,name='login'),
    path('register/',views.Register,name='register'),
    path('forecast',views.streamlit,name='forecast'),
    path('logout',views.logoutUser,name='logout')
]