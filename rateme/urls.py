from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/profile' , views.ProfileList.as_view()) ,
    path('api/project' ,views.ProjectList.as_view() ),

]