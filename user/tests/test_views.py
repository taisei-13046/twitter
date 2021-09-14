from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class HomeViewTests(TestCase):
    """HomeViewのテストクラス"""
    def test_get(self):
        """GET メソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('user:home'))
        self.assertEqual(response.status_code, 200)


class LoginViewTests(TestCase):
    """LoginViewのテストクラス"""
    def test_get(self):
        """GET メソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)


class LogoutViewTests(TestCase):
    """LogoutViewのテストクラス"""
    def test_get(self):
        """GET メソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 200)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        """sampleでユーザを作成"""
        url = reverse('user:signup')
        data = {
            'username': 'example',
            'email': 'sample@example.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('user:home')

    def test_redirection(self):
        """リダイレクト先のページを検証"""
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        """ユーザの作成を検証"""
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        """ログインができているかの検証"""
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        """不適切なユーザを作成"""
        url = reverse('user:signup')
        self.response = self.client.post(url, {})

    def test_signup_status_code(self):
        """ステータスコード200を返されることを確認"""
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        """formエラーの検証"""
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_not_create_user(self):
        """ユーザが存在しないことを確認"""
        self.assertFalse(User.objects.exists())


class LessPasswordSignUpTests(TestCase):
    def setUp(self):
        """短いパスワードのユーザを作成"""
        url = reverse('user:signup')
        data = {
            'username': 'example',
            'email': 'sample@example.com',
            'password1': '123',
            'password2': '123'
        }
        self.response = self.client.post(url, data)

    def test_signup_status_code(self):
        """ステータスコード200を返されることを確認"""
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        """formエラーの検証"""
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_not_create_user(self):
        """ユーザが存在しないことを確認"""
        self.assertFalse(User.objects.exists())
