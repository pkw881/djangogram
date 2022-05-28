from django import forms
from .models import Post, Comment


#우리가 입력받을 데이터가 캡션이랑 이미지임
class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        # 각각 필드 명시
        fields = ["caption", "image"]

        # 레이블 나타내고
        labels = {
            "caption":"내용",
            "image":"사진"
       }
#마무리 되면 뷰로 가서  폼코드 선언 후 템플릿으로 넘기기

#이걸 유저로 넘겨주면 됨
class CommentForm(forms.ModelForm):
    #콘텐츠 미리 정의. 사용자가 보여지는 화면에 레이블인 콘텐츠를 보여주고 싶지 않아서
    # 이부분이 없다면 콘텐츠 레이블이 보여지기 대문에 레이블을 지워주기 위해서
    contents = forms.CharField(widget=forms.Textarea, label = "")

    class Meta:
        # 모델에는 코멘트 명시, 코멘트 모델이니깐.
        model = Comment
        # 각각 필드 명시
        # 필드는 댓글내용만 보여주면 되서 콘텐츠만 명시
        fields = ["contents"]

#마무리 되면 뷰로 가서  폼코드 선언 후 템플릿으로 넘기기



#우리가 입력받을 데이터가 캡션이랑 이미지임
class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        # 각각 필드 명시
        fields = ["caption"]

        # 레이블 나타내고
        labels = {
            "caption":"내용",
       }
