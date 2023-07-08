from django.urls import path
from django.urls import include
from .views import signup, logout_view, change_password
from django.contrib.auth.views import LoginView

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('', signup, name='accounts_home'),
    path('signup/', signup, name='signup'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', logout_view, name='logout'),
    path('change_password/', change_password, name='change_password'),
]