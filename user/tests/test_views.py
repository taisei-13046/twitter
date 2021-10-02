from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY


class HomeViewTests(TestCase):
    """HomeViewのテストクラス"""
    def setUp(self):
        url = reverse('user:signup')
        data = {
            'username': 'example',
            'email': 'sample@example.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)

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
        self.url = reverse('user:signup')

    def test_post_empty_user(self):
        """空のユーザを作成"""
        res = self.client.post(self.url, {})
        self.assertEquals(res.status_code, 200)
        self.assertTrue(res.context.get('form').errors)
        self.assertFalse(User.objects.exists())


class LessPasswordSignUpTests(TestCase):

    def setUp(self):
        """短いパスワードのユーザを作成"""
        self.url = reverse('user:signup')

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

    def test_not_create_user(self):
        """ユーザが存在しないことを確認"""
        self.assertFalse(User.objects.exists())


class LoginTest(TestCase):

    def setUp(self):
        User.objects.create_user('ytaisei', 'example@gmail.com', 'example13046')
        self.url = reverse("user:login")
        self.home_url = reverse("user:home")
        self.client = Client()

    def test_correct_login(self):
        """正しいログイン"""
        data = {
            'username': 'ytaisei',
            'password': 'example13046'
        }
        self.assertNotIn(SESSION_KEY, self.client.session)
        response = self.client.post(self.url, data)

        # 302: リクエストされたリソースが一時的にLocationで示されたURLへ移動したことを示す
        self.assertEqual(response .status_code, 302)
        self.assertRedirects(response, self.home_url)
        self.assertIn(SESSION_KEY, self.client.session)

    def test_incorrect_username_login(self):
        """異なる,存在しないユーザ名でのログイン"""
        data = {
            'username': 'yasui',
            'password': 'example13046'
        }
        response = self.client.post(self.url, data)
        self.assertNotIn(SESSION_KEY, self.client.session)

        self.assertEqual(response .status_code, 200)
        self.assertFormError(response, 'form', '', '正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。')
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_incorrect_password_login(self):
        """間違ったパスワードでのログイン"""
        data = {
            'username': 'ytaisei',
            'password': 'example'
        }
        response = self.client.post(self.url, data)
        self.assertNotIn(SESSION_KEY, self.client.session)

        self.assertEqual(response .status_code, 200)
        self.assertFormError(response, 'form', '', '正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。')
        self.assertNotIn(SESSION_KEY, self.client.session)


class LogoutTest(TestCase):
    """ログアウトのテスト"""
    def setUp(self):
        User.objects.create_user('ytaisei', 'example@gmail.com', 'example13046')
        self.client.login(username='ytaisei', password='example13046')
        self.assertIn(SESSION_KEY, self.client.session)
        self.url = reverse('user:logout')

    def test_success_logout(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('user:signup'))
        self.assertNotIn(SESSION_KEY, self.client.session)


class RedirectNotLoginUser(TestCase):
    """ログインしていない状態で/homeに遷移する"""
    def setUp(self):
        self.home_url = reverse('user:home')

    def test_redirect_not_login_user(self):
        response = self.client.get(self.home_url)
        self.assertRedirects(response, '/login/?next=%2Fhome%2F')
