from django.test import TestCase
from .models import *
# Create your tests here.
class ProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(id = 1, username='mish')
        self.profile = Profile.objects.create(user = self.user,bio = 'impossible is nothing', phone= 2356789)

    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))

    def test_save_profile(self):
        self.assertTrue(isinstance(self.profile,Profile))

    def test_get_profile(self):
        self.profile.save()
        profile = Profile.get_profile()
        self.assertTrue(len(profile) > 0)

class ProjectTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(id = 1, username='kyle')
        self.profile = Profile.objects.create(user = self.user,bio = 'impossible is nothing',phone= 2356789)

        self.project = Project.objects.create(posted_by = self.user,
                                          profile = self.profile,
                                          title = 'Newshiglight',
                                          description='hope it works',
                                          project_link= 'https://totopendonews.herokuapp.com/')

    def test_instance(self):
        self.assertTrue(isinstance(self.project,Project))

    def test_get_projects(self):
        self.project.save()
        project = Project.get_projects()
        self.assertTrue(len(project) == 1)

    def test_find_project(self):
        self.project.save()
        project = Project.find_project('blog')
        self.assertTrue(len(project)  == 0)

