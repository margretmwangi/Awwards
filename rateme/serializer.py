from rest_framework import serializers
from .models import Profile , Project

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','user','profile_photo','bio','phone')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model= Project
        fields =('id','title','posted_by', 'description','project_link')
