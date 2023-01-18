from django.test import TestCase, Client
from http import HTTPStatus

class TestURLAbout(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_about_url_is_working(self):
        '''[ABOUT URLS] Проверяем, что все ссылки приложения работают исправно.'''
        urls = {
            '/about/author/': HTTPStatus.OK,
            '/about/tech/': HTTPStatus.OK
        }
        for url, status in urls.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status, f'Ссылка {url} работает не правильно.')
    
    def test_about_url_is_working(self):
        '''[ABOUT URLS] Проверяем, что все ссылки приложения используют нужные шаблоны.'''
        urls = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html'
        }
        for url, template in urls.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template, f'Ссылка {url} работает c неправильным шаблоном.')
