from django.test import Client, TestCase
from users.forms import CreationForm
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class TestUsersForms(TestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = CreationForm()
        cls.guest_client = Client()
        cls.users_count = User.objects.count()
    
    def test_users_signup_form(self):
        '''[USERS FORM] Проверяем, что при заполнении формы создаётся новый пользователь'''
        form_data = {'username': 'Anfisa', 'password1': 'arbuz123', 'password2': 'arbuz123'}
        self.guest_client.post(reverse('users:signup'), data=form_data, follow=True)
        self.assertEqual(User.objects.count(), self.users_count+1, 'Новые юзеры не создаются')

