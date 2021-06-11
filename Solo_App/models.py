from django.db import models
import bcrypt, re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def validation(self, post_data):
        errors = {}
        if len(post_data['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters."
        if post_data['password'] != post_data['confirm']:
            errors['password'] = 'Your password and Confirm Password do not match.'
        print('gets inside registration val function')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Email is not valid'
        return errors
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())




# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return f"{self.name} {self.alias} {self.email}"

class CommentManager(models.Manager):
    def validate_comment(self, comment_text):
        errors = {}
        if len(comment_text) < 10:
            errors['length'] = 'Comments must be at least 10 characters'
        if len(comment_text) > 1000:
            errors['length'] = f"Comments can be a max of 1000 characters."
        return errors

class Post(models.Model):
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name="liked_comments")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = CommentManager()

class Upload(models.Model):
    file = models.FileField(upload_to="user_images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        default=None
    )

