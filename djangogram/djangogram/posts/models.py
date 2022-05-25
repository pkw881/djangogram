from django.db import models
from djangogram.users import models as user_model

# Create your models here.


class TimestampModel(models.Model):
    create_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        abstract = True

#사진관리하는 모델
class Post(TimestampModel):

    author = models.ForeignKey(
        user_model.User,
        null= True,
        on_delete = models.CASCADE,
        related_name = 'post_author')


    image = models.ImageField(blank = True)
    caption = models.TextField(blank = True)
    image_likes = models.ManyToManyField(
        user_model.User,
        related_name = 'post_image_likes')


# 댓글관리하는 것
class Comment(TimestampModel):
    author = models.ForeignKey(
        user_model.User,
        null= True,
        on_delete = models.CASCADE,
        related_name = 'comment_author')
    posts = models.ForeignKey(
        "Post",
        null= True,
        on_delete = models.CASCADE,
        related_name = 'comment_post')
    contents = models.TextField(blank = True)
