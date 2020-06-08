from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('home/', views.home,name='home'),
    path('profile/(\d+)', views.profile, name='profile'),
    path('new/profile', views.add_profile, name='add_profile'),
    path('search/', views.search_results, name='search_results'),
    path('upload/', views.update_project, name='upload'),
    path('review/(?P<pk>\d+)',views.add_review,name='review'),
    path('all/(?P<pk>\d+)', views.all, name='all'),
    path('api/profile' , views.ProfileList.as_view()) ,
    path('api/project' ,views.ProjectList.as_view() ),
    path('api/profile/profile-id/(?P<pk>[0-9]+)',views.ProfileDescription.as_view()),
    path('api/project/project-id/(?P<pk>[0-9]+)',views.ProjectDescription.as_view())

    

]