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
        self.url = reverse('user:signup')

    def test_post_empty_user(self):
        """空のユーザを作成"""
        res = self.client.post(self.url, {})
        self.assertEquals(res.status_code, 200)
        self.assertTrue(res.context.get('form').errors)
        self.assertFalse(User.objects.filter(username='example').exists())

    def test_post_failed_short_password(self):
        """短いパスワード"""
        less_password_data = {
            'username': 'example',
            'email': 'sample@example.com',
            'password1': '123',
            'password2': '123'
        }
        res = self.client.post(self.url, less_password_data)
        self.assertEquals(res.status_code, 200)
        self.assertTrue(res.context.get('form').errors)
        self.assertFalse(User.objects.filter(username='example').exists())

    def test_post_failed_invalid_email(self):
        """"@のないemail"""
        invalid_email_data = {
            'username': 'example',
            'email': 'sample',
            'password1': '12345678',
            'password2': '12345678'
        }
        res = self.client.post(self.url, invalid_email_data )
        self.assertEquals(res.status_code, 200)
        self.assertTrue(res.context.get('form').errors)
        self.assertFalse(User.objects.filter(username='example').exists())

    def test_post_failed_different_password(self):
        """パスワードが一致していない"""
        different_password_data = {
            'username': 'example',
            'email': 'sample@example.com',
            'password1': '1234',
            'password2': '12345678'
        }
        res = self.client.post(self.url, different_password_data)
        self.assertEquals(res.status_code, 200)
        self.assertTrue(res.context.get('form').errors)
        self.assertFalse(User.objects.filter(username='example').exists())

    def test_post_failed_only_number_password(self):
        """数字のみのパスワード"""
        only_number_password_data = {
            'username': 'example',
            'email': 'sample@example.com',
            'password1': '12345678',
            'password2': '12345678'
        }
        res = self.client.post(self.url, only_number_password_data)
        self.assertEquals(res.status_code, 200)
        self.assertTrue(res.context.get('form').errors)
        self.assertFalse(User.objects.filter(username='example').exists())

    def test_post_failed_like_username_and_password(self):
        """ユーザ名に似たパスワード"""
        like_username_and_password_data = {
            'username': 'example',
            'email': 'sample@example.com',
            'password1': 'example13046',
            'password2': 'example13046'
        }
        res = self.client.post(self.url, like_username_and_password_data)
        self.assertEquals(res.status_code, 200)
        self.assertTrue(res.context.get('form').errors)
        self.assertFalse(User.objects.filter(username='example').exists())

    def test_post_failed_easy_password(self):
        """一般的すぎるパスワード"""
        easy_password_data = {
            'username': 'example',
            'email': 'sample@example.com',
            'password1': 'abcdefghi',
            'password2': 'abcdefghi'
        }
        res = self.client.post(self.url, easy_password_data)
        self.assertEquals(res.status_code, 200)
        self.assertTrue(res.context.get('form').errors)
        self.assertFalse(User.objects.filter(username='example').exists())

    def test_post_duplicate_username(self):
        """重複したユーザ"""
        first_username_data = {
            'username': 'example',
            'email': 'sample@example.com',
            'password1': 'success13046',
            'password2': 'success13046'
        }
        self.client.post(self.url, first_username_data)

        second_username_data = {
            'username': 'example',
            'email': 'sample2@example.com',
            'password1': 'success13046',
            'password2': 'success13046'
        }
        res = self.client.post(self.url, second_username_data)
        self.assertEquals(res.status_code, 200)
        self.assertTrue(res.context.get('form').errors)
