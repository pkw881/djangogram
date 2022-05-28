#공식문서 django rest framwork serializer
#우리는 포스트 모델 타겟이니, 모델에는 포스트모델, 포스트 모델안에 추출할 필드 author image caption comment까지 명시
# 다른건 시리얼라이져 각각 만들어줘야함
# 단순 변환기, Qeuryset같은 것을 네이티브 파이선 형태로 변경시켜줌
# 데이터셋을 제이슨 형식으로 손쉬게 변경가능

from rest_framework import serializers
from djangogram.users.models import User as user_model
from . import models

class FeedAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = (
            "id",
            "username",
            "profile_photo",
        )

class CommentSerializer(serializers.ModelSerializer):
    author = FeedAuthorSerializer()
    class Meta:
        model = models.Comment
        fields = (
            "id",
            "contents",
            "author",
        )



class PostSerializer(serializers.ModelSerializer):
    #모델 시리얼라이져 받아서 우리껄로 만들어보면됨
    comment_post = CommentSerializer(many=True)
    #코멘트와 어서는 다른 모델 사용하니깐 그걸 위에서 만들어줘야함
    author = FeedAuthorSerializer()

    class Meta:
        #우리가 추출하고 싶은 모델 모델의 Post 그리고 추출하고 싶은 필드 각각 작성 id는 장고가 디폴트로 생성
        model = models.Post
        fields = (
            "id",
            "image",
            "caption",
            "comment_post",
            "author",
            "image_likes"

        )
