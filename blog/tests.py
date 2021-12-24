from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

import time
import json


class CreateTweetTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('ytaisei', 'example@gmail.com', 'example13046')

    def setUp(self):
        self.client.login(username='ytaisei', password='example13046')
        self.url = reverse('blog:create')

    def test_with_create_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_success_form(self):
        response = self.client.post(self.url, {'content': 'success'})
        self.assertRedirects(response, reverse('blog:home'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.get(id=1)
        self.assertEqual(post.content, 'success')

    def test_post_empty_form(self):
        response = self.client.post(self.url, {'content': ''})
        self.assertEqual(Post.objects.count(), 0)
        self.assertFormError(response, 'form', 'content', 'このフィールドは必須です。')

    def test_with_over_max_length(self):
        content = 'x' * 141
        self.client.post(self.url, {'content': content})
        self.assertEqual(Post.objects.count(), 0)


class TweetListTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'example@gmail.com', 'example13046')
        self.user2 = User.objects.create_user('user2', 'example@gmail.com', 'example13046')
        self.user1_tweet = Post.objects.create(content='user1', author=self.user1)
        time.sleep(0.1)
        self.user2_tweet = Post.objects.create(content='user2', author=self.user2)
        self.url = reverse('blog:home')

    def test_tweet_list(self):
        self.client.login(username='user1', password='example13046')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['post_list'],
            ['<Post: user2>', '<Post: user1>'],
            ordered=True,
        )
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user1_tweet.content)
        self.assertContains(response, self.user2.username)
        self.assertContains(response, self.user2_tweet.content)


class DetailTweetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('ytaisei', 'example@gmail.com', 'example13046')
        self.client.login(username='ytaisei', password='example13046')
        self.tweet = Post.objects.create(content='detail', author=self.user)
        self.url = reverse('blog:detail', kwargs={'pk': self.tweet.pk})

    def test_tweet_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tweet.content)
        self.assertContains(response, self.user.username)


class UpdateTweetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('ytaisei', 'example@gmail.com', 'example13046')
        self.tweet = Post.objects.create(content='update', author=self.user)
        self.url = reverse('blog:update', kwargs={'pk': self.tweet.pk})

    def test_with_create_view(self):
        self.client.login(username='ytaisei', password='example13046')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_with_correct_update(self):
        self.client.login(username='ytaisei', password='example13046')
        response = self.client.post(self.url, {'content': 'updated tweet'})
        self.assertRedirects(response, reverse('blog:home'))
        post = Post.objects.get(id=self.tweet.pk)
        self.assertEqual(post.content, 'updated tweet')

    def test_post_empty_update_form(self):
        self.client.login(username='ytaisei', password='example13046')
        response = self.client.post(self.url, {'content': ''})
        self.assertFormError(response, 'form', 'content', 'このフィールドは必須です。')

    def test_with_incorrect_user_update(self):
        User.objects.create_user('incorrect', 'example@gmail.com', 'example13046')
        self.client.login(username='incorrect', password='example13046')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)


class DeleteTweetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('ytaisei', 'example@gmail.com', 'example13046')
        self.tweet = Post.objects.create(content='delete', author=self.user)
        self.url = reverse('blog:delete', kwargs={'pk': self.tweet.pk})

    def test_with_delete_view(self):
        self.client.login(username='ytaisei', password='example13046')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_delete_tweet(self):
        self.assertEqual(Post.objects.count(), 1)
        self.client.login(username='ytaisei', password='example13046')
        response = self.client.delete(self.url)
        self.assertRedirects(response, reverse('blog:home'))
        self.assertEqual(Post.objects.count(), 0)

    def test_with_incorrect_user_delete(self):
        User.objects.create_user('incorrect', 'example@gmail.com', 'example13046')
        self.client.login(username='incorrect', password='example13046')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 403)


class LikeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('ytaisei', 'example@gmail.com', 'example13046')
        self.client.login(username='ytaisei', password='example13046')
        self.post = Post.objects.create(content='user1', author=self.user)
        self.url = reverse('blog:like', kwargs={'pk': self.post.pk})

    def test_success_like(self):
        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['count'], 1)
        self.assertEqual(json.loads(response.content)['liked'], True)

    def test_fail_with_like_non_exit_post(self):
        '''
        存在しないpostにlikeしたら404errorが返却される
        '''
        response = self.client.post(reverse('blog:like', kwargs={'pk': 100}), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)

    def test_with_twice_like(self):
        self.client.post(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        time.sleep(0.1)
        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['count'], 1)
        self.assertEqual(json.loads(response.content)['liked'], True)


class UnlikeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('ytaisei', 'example@gmail.com', 'example13046')
        self.client.login(username='ytaisei', password='example13046')
        self.post = Post.objects.create(content='user1', author=self.user)
        self.like_url = reverse('blog:like', kwargs={'pk': self.post.pk})
        self.unlike_url = reverse('blog:unlike', kwargs={'pk': self.post.pk})
        self.like_response = self.client.post(self.like_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

    def test_with_success_unfollow(self):
        self.assertEqual(self.like_response.status_code, 200)
        self.assertEqual(json.loads(self.like_response.content)['count'], 1)
        self.assertEqual(json.loads(self.like_response.content)['liked'], True)
        unlike_response = self.client.post(self.unlike_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(self.like_response.status_code, 200)
        self.assertEqual(json.loads(unlike_response.content)['count'], 0)
        self.assertEqual(json.loads(unlike_response.content)['liked'], False)

    def test_with_twice_unlike(self):
        self.assertEqual(self.like_response.status_code, 200)
        self.assertEqual(json.loads(self.like_response.content)['count'], 1)
        self.assertEqual(json.loads(self.like_response.content)['liked'], True)
        self.client.post(self.unlike_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        time.sleep(0.1)
        unlike_response = self.client.post(self.unlike_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(self.like_response.status_code, 200)
        self.assertEqual(json.loads(unlike_response.content)['count'], 0)
        self.assertEqual(json.loads(unlike_response.content)['liked'], False)

    def test_fail_with_unlike_non_exit_post(self):
        '''
        存在しないpostにunlikeしたら404errorが返却される
        '''
        response = self.client.post(reverse('blog:unlike', kwargs={'pk': 100}), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)
