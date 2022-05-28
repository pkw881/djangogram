from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from djangogram.users.models import User as user_model
from . import models, serializers
from .form import CreatePostForm, CommentForm, UpdatePostForm

# Create your views here.
def index(request):
    # GET 분기
    if request.method == "GET":
        # 인증확인 분기
        if request.user.is_authenticated:
            comment_form = CommentForm()

            # 로그인 한 유저의 포스트와 팔로잉한 유저의 포스트가 보여야함
            # request user id는 로그인된 유저의 아이디 를 유저모델에서 가져오는것
            user = get_object_or_404(user_model, pk = request.user.id)
            # 로그인된 유저사용해서 모든 팔로잉 유저 가져옴
            following = user.following.all()
            #포스트 데이터 가져오는데, 필터에 Q(query)객채 사용해서 "또는" 조건 사용가능
            posts = models.Post.objects.filter(
                Q(author__in=following) | Q(author=user)
            ).order_by("-create_at")
            #시리얼라이저를 선언하고, 여러개가 될 수 있으니 many true 우리가 원하는 방식으로 나오게 함
            #feed main api로직임
            serializer = serializers.PostSerializer(posts, many = True)
            print(serializer.data)

            #위에는 __in 은 팔로잉이 여러명이면 모두 가져오는것(in contain gt startswith 존재)
            #우ㅢ에서 코멘트 폼 만들고 아래에 렌더에 코멘트 폼 넘겨주기기
            #커멘트 폼을 탬플릿에 넘겨줬으니 html가서 정리
            return render(request,'posts/main.html', {"posts":serializer.data, "comment_form":comment_form})


def post_create(request):
    #사용자가 페이지 요청하는것
    if request.method == "GET":
        # 우리가 작성한 폼 선언
        form = CreatePostForm()
        # 템플릿으로 넘겨주는데, 위치는 사용자가 개시물 등록을 위해 화면을 요청하는데가
        # Get이니깐 거기다 요청해서 템플릿으로 넘겨서 렌더 하는것
        # 포스트 크리에잇 호출
        return render(request, 'posts/post_create.html', {"form":form})

    elif request.method == "POST":
        # 유저가 인증되었는지 판단
        if request.user.is_authenticated:
            # 유저 아이디 사용해서 유저 가져오기
            user = get_object_or_404(user_model, pk=request.user.id)

            # # 다음으로 요청받은 데이터 가져오기
            # # 파일데이터는 파일즈를 사용 이외의 데이터는 포스트 필드 사용함
            # image = request.FILES['image']
            # # 캡션은 포스트에서 가져온다
            # caption = request.POST['caption']
            #
            # # 포스트를 만들도록 하는데 명심할 것은 아래 save 기능
            # new_post = models.Post.objects.create(
            #     author = user,
            #     image = image,
            #     caption = caption
            # )
            # new_post.save()

            # 폼을 활용하는 방식
            # 픔올 활용해서 요청받은 포스트와 파일을 넘겨주고
            form = CreatePostForm(request.POST, request.FILES)
            #유효성 검사후 바로 저장
            if form.is_valid():
                # 커밋 팔스는 데이터가 디비에 저장안되고 포스트 데이터 만드는것
                # 특정 작업 후 세이브 하면 저장되는 형태
                post = form.save(commit = False)
                # 오써는 포린키라 여기서 받은게 아님 그래서 유저를 씀
                post.author = user
                post.save()
            else :
                print(form.errors)

            # 포스트 생성하면 포스트 페이지로 이동되게 함
            return redirect(reverse('posts:index'))

        # 로그인 안되어있으면 유저의 메인페이지로 이동하게 함
        else:
            return render(request, 'users/main.html')

#url에서 전달받은 포스트아이디를 인자로 받아서
def comment_create(request, post_id):
    #해당 아이디로 포스트 아이디를 검색
    if request.user.is_authenticated:
        #장고에서 데이터 생성될때 테이블마다 유일값 부여
        post=get_object_or_404(models.Post, pk=post_id)

        #유져가 입력한건 리케스트 포스트에담겨 있고 이걸 코멘트 폼에 전달
        form = CommentForm(request.POST)
        # 폼사용에서는 유효성 검사 이스벨리드
        if form.is_valid():
            #코멘트를 생성하면 됨
            # commit명령어는 데이터베이스 디스크에 데이터를 입력하겠다임
            # false는 데이터베이스 디스크에는 입력안되어있음
            # 댓글 폼에는 댓글에대한 내용만 저자되어있어서 어서와 포스트 입력후 save함수를 통해 커밋 실시
            # 커밋 입력안하면 true가 디폴트
            comment = form.save(commit=False)
            comment.author = request.user
            comment.posts = post
            comment.save()
            # feed페이지 로 넘겨주고 index 엘리어서 샵 커맨트, 뒤에 입력되어있으면 html아이디 선택자가 명시된 부분으로 스크롤이 내려짐
            # 탬플릿 작성시 댓글 부분에 아이디 부분에 사전 입력해놓음
            return redirect(reverse('posts:index') + "#comment-" + str(comment.id))
        else :
            return render(request, 'users/main.html')

def comment_delete(request, comment_id):
    #해당 아이디로 포스트 아이디를 검색
    if request.user.is_authenticated:
        #전달받은 댓글에서 서버에 댓글 존재하는 지 확인하고 존재하면 현재 사용하는 사용자 댓글 확인
        comment = get_object_or_404(models.Comment, pk=comment_id)
        # 현재 유저의 댓글인지 확인
        if request.user == comment.author:
            comment.delete()

        return redirect(reverse('posts:index'))
        #장고에서 데이터 생성될때 테이블마다 유일값 부여

    else:
        return render(request, 'users/main.html')

def post_delete(request, post_id):
    #사용자가 페이지 요청하는것
    if request.user.is_authenticated :
        post = get_object_or_404(models.Post, pk=post_id)
        if request.user == post.author:
            post.delete()
        return redirect(reverse('posts:index'))
    else :
        return render(request, 'users/main.html')

def post_update(request, post_id):
    #사용자가 페이지 요청하는것
    if request.user.is_authenticated :
        #데이터 베이스에서 포스ㅡㅌ 가져오고 키값이 포스트 아이디로 줘서 조회
        # 포스트 데이터 찾아오기
        post = get_object_or_404(models.Post, pk=post_id)
        #작성자 체크
        if request.user != post.author:
            return redirect(reverse('posts:index'))

        # 폼을넘겨주기 전에는 폼에 방금 추출한 포스트를 명시 해주면 화면 폼 내에 데이터 베이스에서 추출한 데이터가 보임
        # 수정전 데이터가 보여지는걸 위해서 추출한 포스트를 폼에 넘겨주기
        if request.method == 'GET':
            form = UpdatePostForm(instance=post)
            return render(request,
                          'posts/post_update.html',
                          {"form":form, "post":post})

        # 데이터 저장방식의 전송방식은 POST방식임
        elif request.method == "POST":
            form = UpdatePostForm(request.POST)
            #유효성 검사후 바로 저장
            if form.is_valid():
                # form에 클린드 데이터로 부터 키값을 입력받아서 사용
                post.caption = form.cleaned_data['caption']
                #앞쪽에서 조회한 포스트 를 세확인하고 세이브
                post.save()
            return redirect(reverse('posts:index'))
    else :
        return render(request, 'users/main.html')



def post_like(request, post_id):
    #사용자가 페이지 요청하는것
    # ajax활용해서 jason내려주는거라 리스폰스 만들자
    response_body = {"result": ""}

    if request.user.is_authenticated :
        if request.method=="POST":
            post = get_object_or_404(models.Post, pk = post_id)

            #user가 포스트 좋아요 누른 상태라면 exsited user가 트루임. 왜
            existed_user = post.image_likes.filter(pk=request.user.id).exists()
            if existed_user:
                post.image_likes.remove(request.user)
                response_body["result"] = "dislike"
            else:
                post.image_likes.add(request.user)
                response_body["result"] = "like"

            post.save()
            return JsonResponse(status = 200, data = response_body)
    else :
        return JsonResponse(status = 403, data = response_body)

def search(request):
    if request.user.is_authenticated :
        if request.method == "GET":
            #리퀘스트로 들어온 겟 방식에서 q키의 값을 도출하라
            # 그리고 남은건 인덱스 함수의 로직과 매우 유사
            searchKeyword = request.GET.get("q", "")

            comment_form = CommentForm()
            # 로그인 한 유저의 포스트와 팔로잉한 유저의 포스트가 보여야함
            # request user id는 로그인된 유저의 아이디 를 유저모델에서 가져오는것
            user = get_object_or_404(user_model, pk = request.user.id)
            # 로그인된 유저사용해서 모든 팔로잉 유저 가져옴
            following = user.following.all()
            #포스트 데이터 가져오는데, 필터에 Q(query)객채 사용해서 "또는" 조건 사용가능
            # 포스트를 검색할때 사용자가 입력한 키워드를 추가 해서 가져 오는것
            posts = models.Post.objects.filter(
                (Q(author__in=following) | Q(author=user)) & Q(caption__contains=searchKeyword)
            ).order_by("-create_at")
            #시리얼라이저를 선언하고, 여러개가 될 수 있으니 many true 우리가 원하는 방식으로 나오게 함
            #feed main api로직임
            serializer = serializers.PostSerializer(posts, many = True)
            print(serializer.data)

            #위에는 __in 은 팔로잉이 여러명이면 모두 가져오는것(in contain gt startswith 존재)
            #우ㅢ에서 코멘트 폼 만들고 아래에 렌더에 코멘트 폼 넘겨주기기
            #커멘트 폼을 탬플릿에 넘겨줬으니 html가서 정리
            return render(request,'posts/main.html', {"posts":serializer.data, "comment_form":comment_form})


    else:
        return render(request, 'users/main.html')

    pass

