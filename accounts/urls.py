from django.urls import path
from . import views



urlpatterns = [
    
    path('singup/', views.UserRegister.as_view(), name="signup"),
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('logout/', views.logoutView.as_view(), name="logout"),
    path('deposite/', views.depositeView, name="deposite"),
    path('profile/', views.profile, name="profile"),
    
]