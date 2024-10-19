from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    token = models.TextField(blank=True, null=True)



class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    description = models.TextField()
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)



class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)