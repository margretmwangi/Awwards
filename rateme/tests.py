from django.test import TestCase
from .models import *
# Create your tests here.
class ProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(id = 1, username='zyzu')
        self.profile = Profile.objects.create(user = self.user,bio = 'blow away', phone= 2356789)

    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))

    def test_save_profile(self):
        self.assertTrue(isinstance(self.profile,Profile))

    def test_get_profile(self):
        self.profile.save()
        profile = Profile.get_profile()
        self.assertTrue(len(profile) > 0)