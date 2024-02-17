from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from webapp.models import UserStats, Sessions
from django.contrib.messages import get_messages
from rest_framework.test import APIClient
from datetime import datetime, timedelta

import json

class RegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('webapp:register')

    def test_registration_success(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Check if redirect
        self.assertEqual(get_user_model().objects.count(), 1)  # Check if user created
        self.assertEqual(UserStats.objects.count(), 1)  # Check if UserStats created

    def test_registration_failure(self):
        response = self.client.post(self.register_url, {
            'username': '',
            'email': 'testuser@gmail.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 200)  # Check if staying on same page

        # Check if error message was added
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'There was a problem with your registration.')

    
class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('webapp:login')
        self.test_user = get_user_model().objects.create_user(username='testuser', email='testuser@gmail.com', password='testpassword123', preferred_mode='light')

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Check if redirect
        self.assertEqual(int(self.client.session['_auth_user_id']), self.test_user.pk)  # Check if user is logged in

    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'testpassword123',
        })
        self.assertEqual(response.status_code, 200)  # Check if staying on same page
        self.assertNotIn('_auth_user_id', self.client.session)  # Check if user is not logged in


class LogoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('webapp:logout')
        self.test_user = get_user_model().objects.create_user(username='testuser', email='testuser@gmail.com', password='testpassword123', preferred_mode='light')
        self.client.login(username='testuser', password='testpassword123')  # Log in the user

    def test_logout(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Check if redirect
        self.assertNotIn('_auth_user_id', self.client.session)  # Check if user is logged out

class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = get_user_model().objects.create_user(username='testuser', email='testuser@gmail.com', password='testpassword123', preferred_mode='light')
        self.client.login(username='testuser', password='testpassword123')  # Log in the user
        self.user_stats = UserStats.objects.create(user=self.test_user)  # Create UserStats for the user

    def test_index(self):
        response = self.client.get(reverse('webapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.test_user)

    def test_breathe(self):
        response = self.client.get(reverse('webapp:breathe'))
        self.assertEqual(response.status_code, 200)

    def test_meditate(self):
        response = self.client.get(reverse('webapp:meditate'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['music_types'], {0: 'No Sound', 1: 'Fireplace', 2: 'Rain in Forest', 3: 'Rain', 4: 'River'})

    def test_stats(self):
        response = self.client.get(reverse('webapp:stats'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['stats'], self.user_stats)

    def test_play_music(self):
        response = self.client.get(reverse('webapp:play_music'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp/play_music.html')

    def test_play_session(self):
        response = self.client.get(reverse('webapp:play_session'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp/play_session.html')

class APITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = get_user_model().objects.create_user(username='testuser', email='testuser@gmail.com', password='testpassword123', preferred_mode='light')
        self.client.login(username='testuser', password='testpassword123')  # Log in the user
        self.user_stats = UserStats.objects.create(user=self.test_user)  # Create UserStats for the user

    def test_update_mode_api(self):
        response = self.client.post(reverse('webapp:update_mode_api'), {'preferred_mode': 'dark'})
        self.assertEqual(response.status_code, 200)
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.preferred_mode, 'dark')

    def test_update_session_api(self):
        session_data = {
            'end_time': "2024-02-17T04:03:59.505Z",
            'session_type': "Meditation Session",
            'start_time': "2024-02-17T04:02:59.505Z",
        }

        json_data = json.dumps(session_data)

        response = self.client.post(reverse('webapp:update_session_api'), json_data, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Sessions.objects.count(), 1)
        self.assertEqual(UserStats.objects.get(user=self.test_user).total_sessions, 1)

    def test_get_active_days_api(self):
        Sessions.objects.create(username=self.test_user,
                                start_time=datetime.utcnow(),
                                end_time=datetime.utcnow() + timedelta(hours=1),
                                duration=60,
                                session_type='Breathing Session',
                                streak=1)
        response = self.client.get(reverse('webapp:get_active_days_api'), {'month': datetime.now().month, 'year': datetime.now().year})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['active_days'], [datetime.now().day])
        self.assertEqual(len(response.data['sessions']), 1)