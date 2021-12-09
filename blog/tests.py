from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

import time
# Create your tests here.


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


class FollowTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'example@gmail.com', 'example13046')
        self.user2 = User.objects.create_user('user2', 'example@gmail.com', 'example13046')
        self.url1 = reverse('blog:follow', kwargs={'username': self.user1.username})
        self.url2 = reverse('blog:follow', kwargs={'username': self.user2.username})

    def test_success_create_follow(self):
        self.client.login(username='user1', password='example13046')
        response = self.client.post(self.url2, {'follow': 'follow'})
        self.assertEqual(response.status_code, 200)
        following_list = self.user1.following.values_list('follow_to')
        following = User.objects.filter(id__in=following_list)
        for following_name in following:
            self.assertEqual(following_name.username, self.user2.username)

    def test_success_delete_follow(self):
        self.client.login(username='user1', password='example13046')
        follow_response = self.client.post(self.url2, {'follow': 'follow'})
        self.assertEqual(follow_response.status_code, 200)
        following_list = self.user1.following.values_list('follow_to')
        following = User.objects.filter(id__in=following_list)
        for following_name in following:
            self.assertEqual(following_name.username, self.user2.username)

        unfollow_response = self.client.post(self.url2, {'unfollow': 'unfollow'})
        self.assertEqual(unfollow_response.status_code, 200)
        following_count = User.objects.filter(id__in=following_list).count()
        self.assertEqual(following_count, 0)

    def test_fail_create_follow(self):
        self.client.login(username='user1', password='example13046')
        follow_response = self.client.post(self.url1, {'follow': 'follow'})
        self.assertEqual(follow_response.status_code, 404)
        following_list = self.user1.following.values_list('follow_to')
        following_count = User.objects.filter(id__in=following_list).count()
        self.assertEqual(following_count, 0)
