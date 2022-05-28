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
        #실제 데이터 베이스 관련
        null= True,
        on_delete = models.CASCADE,
        related_name = 'post_author')

    # 여기에 FAlse 들어가면, 블랭크는 저장안되도록 하는것
    image = models.ImageField(blank = False)
    caption = models.TextField(blank = False)
    image_likes = models.ManyToManyField(
        user_model.User,
        blank=True,
        related_name = 'post_image_likes')

    def __str__(self):
        return f"{self.author}:{self.caption}"



# 댓글관리하는 것
class Comment(TimestampModel):
    author = models.ForeignKey(
        user_model.User,
        null= True,
        on_delete = models.CASCADE,
        related_name = 'comment_author')
    #포스트를 외래키로 사용하고 있음
    posts = models.ForeignKey(
        "Post",
        null= True,
        on_delete = models.CASCADE,
        related_name = 'comment_post')
    contents = models.TextField(blank = True)

    def __str__(self):
        return f"{self.author}:{self.contents}"
