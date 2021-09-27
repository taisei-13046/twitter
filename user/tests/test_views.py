from django.test import TestCase, Client
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


class LoginTest(TestCase):

    def setUp(self):
        User.objects.create_user('ytaisei', 'example@gmail.com', 'example13046')
        self.url = reverse("user:login")
        self.home_url = reverse("user:home")

    def test_correct_login(self):
        """正しいログイン"""
        data = {
            'username': 'ytaisei',
            'password': 'example13046'
        }
        response = self.client.post(self.url, data)

        # 302: リクエストされたリソースが一時的にLocationで示されたURLへ移動したことを示す
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

    def test_incorrect_username_login(self):
        """異なる,存在しないユーザ名でのログイン"""
        data = {
            'username': 'yasui',
            'password': 'example13046'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', '', '正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。')

    def test_incorrect_password_login(self):
        """間違ったパスワードでのログイン"""
        data = {
            'username': 'ytaisei',
            'password': 'example'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', '', '正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。')


class LogoutTest(TestCase):
    """ログアウトのテスト"""
    def setUp(self):
        User.objects.create_user('ytaisei', 'example@gmail.com', 'example13046')
        self.client.login(username='ytaisei', password='example13046')
        self.url = reverse('user:logout')

    def test_success_logout(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('user:signup'))
