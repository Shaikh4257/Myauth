from django.urls import path
from accounts import views


urlpatterns = [
    path('', views.start, name="home" ),
    path('signup', views.register, name="signup"),
    path('signin', views.signin, name="signin"),
    path('dashboard/', views.dashboard, name="dashboard" ),
    path('dashboard/updateprofile', views.UpdateProfile, name="updateprofile" ),
    path('dashboard/settings', views.changePassword, name="changepassword" ),
    path('dashboard/search', views.search, name="search" ),
    path('signout', views.Logout, name="Logout"),
]