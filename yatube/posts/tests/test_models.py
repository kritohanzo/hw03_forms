from posts.models import Post, Group
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост Тестовый пост Тестовый пост'
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        group = PostModelTest.group
        post_str = str(post)
        expected_post_str = post.text[:15]
        self.assertEqual(post_str, expected_post_str)
        group_str = str(group)
        expected_group_str = group.title
        self.assertEqual(group_str, expected_group_str)
    
    def test_models_have_correct_verbose_name(self):
        """Проверяем, что у моделей корректно работает verbose_name."""
        post = PostModelTest.post
        field_verbose_names = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа'
        }
        for field, expected_value in field_verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(post._meta.get_field(field).verbose_name, expected_value)
    
    def test_models_have_correct_help_text(self):
        """Проверяем, что у моделей корректно работает help_text."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Текст поста, который увидят пользователи',
            'group': 'Группа, к которой будет относиться запись'
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(post._meta.get_field(field).help_text, expected_value)