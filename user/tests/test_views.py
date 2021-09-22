from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

import unittest


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


class NoneSignUpTests(TestCase):
    def setUp(self):
        """不適切なユーザを作成"""
        url = reverse('user:signup')
        self.response = self.client.post(url, {})

    def test_signup_status_code(self):
        """無効なフォームを送信した場合、同じページに戻る"""
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        """formエラーの検証"""
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_not_create_user(self):
        """ユーザが存在しないことを確認"""
        self.assertFalse(User.objects.exists())


class InvalidSignUpTests(TestCase):
    def setUp(self):
        """さまざまなエラーの出るユーザを作成"""
        url = reverse('user:signup')
        """短いパスワード"""
        less_password_data = {
            'username': 'example',
            'email': 'sample@example.com',
            'password1': '123',
            'password2': '123'
        }
        self.less_password_response = self.client.post(url, less_password_data)

        """"@のないemail"""
        invalid_email_data = {
            'username': 'example',
            'email': 'sample',
            'password1': '12345678',
            'password2': '12345678'
        }
        self.invalid_email_response = self.client.post(url, invalid_email_data)

        """パスワードが一致していない"""
        different_password_data = {
            'username': 'example',
            'email': 'sample@example.com',
            'password1': '1234',
            'password2': '12345678'
        }
        self.different_password_response = self.client.post(url, different_password_data)

        """数字のみのパスワード"""
        only_number_password_data = {
            'username': 'example',
            'email': 'sample@example.com',
            'password1': '12345678',
            'password2': '12345678'
        }
        self.only_number_password_response = self.client.post(url, only_number_password_data)

        """ユーザ名に似たパスワード"""
        like_username_and_password_data = {
            'username': 'example',
            'email': 'sample@example.com',
            'password1': 'example13046',
            'password2': 'example13046'
        }
        self.like_username_and_password_response = self.client.post(url, like_username_and_password_data)

        """一般的すぎるパスワード"""
        easy_password_data = {
            'username': 'example',
            'email': 'sample@example.com',
            'password1': 'abcdefghi',
            'password2': 'abcdefghi'
        }
        self.easy_password_data_response = self.client.post(url, easy_password_data)

    def test_signup_status_code(self):
        """ステータスコード200を返されることを確認"""
        self.assertEquals(self.less_password_response.status_code, 200)
        self.assertEquals(self.invalid_email_response.status_code, 200)
        self.assertEquals(self.different_password_response.status_code, 200)
        self.assertEquals(self.only_number_password_response.status_code, 200)
        self.assertEquals(self.like_username_and_password_response.status_code, 200)
        self.assertEquals(self.easy_password_data_response.status_code, 200)

    def test_form_errors(self):
        """formエラーの検証"""
        less_password_form = self.less_password_response.context.get('form')
        self.assertTrue(less_password_form.errors)

        invalid_email_form = self.invalid_email_response.context.get('form')
        self.assertTrue(invalid_email_form.errors)

        different_password_form = self.different_password_response.context.get('form')
        self.assertTrue(different_password_form.errors)

        only_number_password_form = self.only_number_password_response.context.get('form')
        self.assertTrue(only_number_password_form.errors)

        like_username_and_password_form = self.like_username_and_password_response.context.get('form')
        self.assertTrue(like_username_and_password_form.errors)

        easy_password_data_form = self.easy_password_data_response.context.get('form')
        self.assertTrue(easy_password_data_form.errors)

    def test_not_create_user(self):
        """ユーザが存在しないことを確認"""
        self.assertFalse(User.objects.exists())
