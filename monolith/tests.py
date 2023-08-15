from django.test import TestCase
from django.urls import reverse
# Create your tests here.
from .models import *

class GuildModelTests(TestCase):
    def test_str_method(self):
        guild = Guild(name="TestGuild")
        guild.save()
        self.assertEqual(str(guild),"TestGuild: 0 users")

class IndexViewTests(TestCase):
    def test_index_no_user(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
    

    