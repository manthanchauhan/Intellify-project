from django.urls import path
from customusers import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('all', views.users_list),
]

urlpatterns = format_suffix_patterns(urlpatterns=urlpatterns)