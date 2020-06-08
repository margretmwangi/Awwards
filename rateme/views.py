 
from django.shortcuts import render,redirect,get_object_or_404
from django.http  import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from rest_framework import status
from .permissions import IsAdminOrReadOnly
# Create your views here.



class ProfileList(APIView):

    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)


    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        permission_classes = (IsAdminOrReadOnly,)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)

class ProjectList(APIView):
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProjectSerializer(data=request.data)
        permission_classes = (IsAdminOrReadOnly,)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

def registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}')
            return redirect('home/')
    else :

        form = UserRegisterForm()
    return render(request,'registration/registration_form.html' , {'form':form})

def login(request):
    return render(request, 'registration/login.html') 

def home(request):
    projects = Project.get_projects()
    reviews = Reviews.get_reviews()
    profile = Profile.get_profile()

    current_user = request.user
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            design = form.cleaned_data['design']
            usability = form.cleaned_data['usability']
            content = form.cleaned_data['content']
            review = form.save(commit=False)
            review.project = project
            review.juror = current_user
            review.design = design
            review.usability = usability
            review.content = content
            review.save()
        return redirect('home/')

    else:
        form = ReviewForm()

    return render(request,"home.html",{"projects":projects, "reviews":reviews,"form": form,"profile":profile})

class ProjectDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_project(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        project= self.get_project(pk)
        serializers = ProjectSerializer(project)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        project = self.get_project(pk)
        serializers = ProjectSerializer(project, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_project(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def all(request, pk):
    profile = Profile.objects.get(pk=pk)
    projects = Project.objects.all().filter(posted_by_id=pk)
    content = {
        "profile": profile,
        'projects': projects,
    }
    return render(request, 'profile.html', content)
def add_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return redirect('home/')

    else:
        form = NewProfileForm()
    return render(request, 'new_profile.html', {"form": form})

def update_project(request):
    current_user = request.user
    profiles = Profile.get_profile()
    for profile in profiles:
        if profile.user.id == current_user.id:
            if request.method == 'POST':
                form = UploadForm(request.POST,request.FILES)
                if form.is_valid():
                    upload = form.save(commit=False)
                    upload.posted_by = current_user
                    upload.profile = profile
                    upload.save()
                    return redirect('home/')
            else:
                form = UploadForm()
            return render(request,'upload.html',{"user":current_user,"form":form})

def add_review(request,pk):
    project = get_object_or_404(Project, pk=pk)
    current_user = request.user
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            design = form.cleaned_data['design']
            usability = form.cleaned_data['usability']
            content = form.cleaned_data['content']
            review = form.save(commit=False)
            review.project = project
            review.juror = current_user
            review.design = design
            review.usability = usability
            review.content = content
            review.save()
            return redirect('home/')
    else:
        form = ReviewForm()
        return render(request,'review.html',{"user":current_user,"form":form})

def search_results(request):

    if 'title' in request.GET and request.GET["title"]:
        search_term = request.GET.get("title")
        searched_project = Project.find_project(search_term)
        message = search_term

        return render(request,'search.html',{"message":message,
                                             "searched_project":searched_project})
    else:
        message = "You haven't searched for any project"
        return render(request,'search.html',{"message":message})
def profile(request,profile_id):

    profile = Profile.objects.get(pk = profile_id)
    projects = Project.objects.filter(profile_id=profile).all()

    return render(request,"profile.html",{"profile":profile,"projects":projects})