from django.test import TestCase, Client
from posts.models import Post, Group
from posts.forms import PostForm
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class TestFormsPosts(TestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostForm()
        cls.user = User.objects.create_user(username='Dimon')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-group',
            description='Описание тестовой группы'
        )
        cls.post = Post.objects.create(
            text='Тестовый пост 123',
            author=cls.user
        )


    def test_posts_forms_create_new_posts_if_valid(self):
        '''[POSTS FORMS] Проверяем, что в случае отправки валидной формы создаётся новый пост в базе данных.'''
        posts_count = Post.objects.count()
        form_data = {'text': 'Тестовый пост'}
        response = self.auth_client.post(reverse('posts:post_create'), data=form_data, follow=True)
        self.assertEqual(Post.objects.count(), posts_count+1, 'Посты не создаются')
        self.assertTrue(Post.objects.filter(text='Тестовый пост', author=self.user.id).exists(), 'Посты не создаются')

    def test_posts_forms_can_edit_posts_if_valid(self):
        '''[POSTS FORMS] Проверяем, что в случае отправки валидной формы редактируется пост в базе данных.'''
        form_data = {'text': 'Уже не тестовый пост =)', 'group': self.group.id}
        response = self.auth_client.post(reverse('posts:post_edit', kwargs={'post_id': self.post.id}), data=form_data, follow=True)
        edited_post = Post.objects.get(id=self.post.id)
        self.assertEqual(edited_post.text, form_data['text'], 'Текст поста не изменился')
        self.assertEqual(edited_post.group.id, form_data['group'], 'Группа поста не изменилась')