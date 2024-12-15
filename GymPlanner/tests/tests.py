from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from trainer.models import Trainer
from training.models import Training, Exercise
from user.models import CustomUser


class TrainerTests(APITestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(
            username='Admin',
            email='a@mail.ru',
            password='12345'
        )
        self.user = CustomUser.objects.create_user(
            username='Lesha',
            email='l@mail.ru',
            password='12345'
        )
        self.refresh_user = RefreshToken.for_user(self.user)
        self.access_token_user = str(self.refresh_user.access_token)
        self.refresh_admin = RefreshToken.for_user(self.admin)
        self.access_token_admin = str(self.refresh_admin.access_token)
        self.trainer_data = {
            'first_name': 'Vadim',
            'last_name': 'Raidiuk',
            'years': 23,
            'year_of_exp': 3,
            'bio': 'test text'
        }
        self.trainer = Trainer.objects.create(**self.trainer_data)
        self.url = '/api/trainers/'

    def test_only_admin_can_create_trainer(self):
        response_admin = self.client.post(
            self.url,
            self.trainer_data,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token_admin}'
        )
        response_user = self.client.post(
            self.url,
            self.trainer_data,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token_user}'
        )
        self.assertEqual(response_admin.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_of_trainers(self):
        url = reverse('trainer-list')
        response_admin = self.client.get(
            url,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token_admin}'
        )
        response_user = self.client.get(
            url,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token_user}'
        )
        self.assertEqual(response_admin.status_code, 200)
        self.assertEqual(response_user.status_code, 200)
        self.assertEqual(len(list(response_admin)), 1)
        self.assertEqual(len(list(response_user)), 1)

    def test_only_admin_can_update_trainer(self):
        update_url = reverse(
            'trainer-detail',
            kwargs={'pk':self.trainer.pk}
        )
        response_admin = self.client.patch(
            update_url,
            {'first_name': 'Vitaly'},
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token_admin}'
        )
        response_user = self.client.patch(
            update_url,
            {'first_name': 'Vitaly'},
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token_user}'
        )
        self.assertEqual(response_admin.status_code, 200)
        self.assertEqual(response_admin.data['first_name'], 'Vitaly')
        self.assertEqual(response_user.status_code, 403)

    def test_only_admin_can_delete_trainer(self):
        delete_url = reverse('trainer-detail', kwargs={'pk':self.trainer.pk})
        response_admin = self.client.delete(
            delete_url,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token_admin}'
        )
        response_user = self.client.delete(
            delete_url,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token_user}'
        )
        self.assertEqual(response_admin.status_code, 204)
        self.assertEqual(response_user.status_code, 403)


class TrainingViewSetTest(APITestCase):

    def setUp(self):
        self.admin_user = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@mail.com',
            password='adminpassword'
        )
        self.client_user = CustomUser.objects.create_user(
            username='client',
            email='client@mail.com',
            password='clientpassword',
            role='client'
        )
        self.trainer = Trainer.objects.create(
            first_name="Vadim",
            last_name="Raidiuk",
            years=23,
            year_of_exp=3,
            bio="test bio"
        )
        self.exercise = Exercise.objects.create(
            title="Push-up",
            description="A basic bodyweight exercise",
            amount_sets=3,
            repetitions=15
        )
        self.training = Training.objects.create(
            title="Big muscles",
            type="power",
            level="beginner",
            duration=30,
            description="Strength training for beginners",
            trainer=self.trainer
        )
        self.training.exercises.set([self.exercise])
        self.refresh_admin = RefreshToken.for_user(self.admin_user)
        self.access_token_admin = str(self.refresh_admin.access_token)
        self.refresh_client = RefreshToken.for_user(self.client_user)
        self.access_token_client = str(self.refresh_client.access_token)

    def test_admin_can_create_training(self):
        data = {
            'title': 'Advanced Training',
            'type': 'power',
            'level': 'advanced',
            'duration': 45,
            'description': 'Advanced strength training',
            'trainer': self.trainer.id,
            'exercises': [self.exercise.id]
        }
        response_admin = self.client.post(
            '/api/trainings/',
            data,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token_admin}'
        )
        response_client = self.client.post(
            '/api/trainings/',
            data,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token_client}'
        )
        self.assertEqual(response_admin.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_client.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_client_and_admin_can_view_training(self):
        response_client = self.client.get(
            '/api/trainings/',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token_client}'
        )
        response_admin = self.client.get(
            '/api/trainings/',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token_admin}'
        )
        response_guest = self.client.get('/api/trainings/')
        self.assertEqual(response_admin.status_code, 200)
        self.assertEqual(response_client.status_code, 200)
        self.assertEqual(response_guest.status_code, 401)

    def test_only_admin_can_update_training(self):
        update_url = reverse(
            'trainings-detail',
            kwargs={'pk':self.training.pk}
        )
        response_admin_update = self.client.patch(
            update_url, {'title':'New title'},
            HTTP_AUTHORIZATION=f'Bearer {self.access_token_admin}'
        )
        response_client_update = self.client.patch(
            update_url, {'title': 'New title'},
            HTTP_AUTHORIZATION=f'Bearer {self.access_token_client}'
        )
        response_unauth_update = self.client.patch(
            update_url,
            {'title': 'New title'}
        )
        self.assertEqual(response_admin_update.status_code, 200)
        self.assertEqual(response_client_update.status_code, 403)
        self.assertEqual(response_unauth_update.status_code, 401)