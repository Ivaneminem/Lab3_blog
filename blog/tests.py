from django.test import TestCase
from django.urls import reverse
from .models import Post, Author, Comment

class PostModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author", email="testauthor@example.com")
        self.post = Post.objects.create(title="Test Title", content="Test Content", author=self.author)

    def test_post_creation(self):
        post = Post.objects.get(title="Test Title")
        self.assertEqual(post.title, "Test Title")
        self.assertEqual(post.author.name, "Test Author")

class PostViewTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author", email="testauthor@example.com")
        self.post = Post.objects.create(title="Test Title", content="Test Content", author=self.author)

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertContains(response, self.post.title)

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, self.post.title)

    def test_post_create_view(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'New Post',
            'content': 'New Content',
            'author': self.author.id
        })
        self.assertEqual(response.status_code, 302)  # Перевірка на перенаправлення після створення
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_post_update_view(self):
        response = self.client.post(reverse('post_update', kwargs={'pk': self.post.pk}), {
            'title': 'Updated Title',
            'content': 'Updated Content',
            'author': self.author.id
        })
        self.assertEqual(response.status_code, 302)  # Перевірка на перенаправлення після оновлення
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')

    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)  # Перевірка на перенаправлення після видалення
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

class CommentViewTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author", email="testauthor@example.com")
        self.post = Post.objects.create(title="Test Title", content="Test Content", author=self.author)
        self.comment = Comment.objects.create(post=self.post, author=self.author, content="Test Comment")

    def test_comment_create_view(self):
        response = self.client.post(reverse('add_comment', kwargs={'pk': self.post.pk}), {
            'content': 'New Comment',
            'author': self.author.id
        })
        self.assertEqual(response.status_code, 302)  # Перевірка на перенаправлення після створення коментаря
        self.assertTrue(Comment.objects.filter(content='New Comment').exists())
