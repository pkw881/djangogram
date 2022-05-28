from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

class TestPosts(TestCase):
    # 테스트 코드 동작전에 필요 데이터 생성 및 초기화 하는 단계
    # 셋업부터 수행 된 후 테스트 수행
    def setUp(self):
        # user 모델 가져와서
        user = get_user_model()
        # user 생성한다
        self.user = user.objects.create_user(
            username='jungo', email='jungo@gmail.com', password="top_secret"
        )

    def test_get_posts_page(self):
        url = reverse('posts:post_create')
        # 우리의 역할을 대신하는 클라이언트는 url요청함
        response = self.client.get(url)

        # 위 결과값이 정상적인 200번인가
        self.assertEqual(response.status_code, 200)
        # 화면은 포스트 크리에이트 템플릿이 사용된느가 확인
        self.assertTemplateUsed(response, 'posts/post_create.html')

    # 포스트가 정상 생성되는 테스트 수행
    def test_creating_posts(self):
        # 로그인 되는지 테스트
        login = self.client.login(username='jungo', password="top_secret")
        # 로그인 후 트루인지 확인
        self.assertTrue(login)

        # 포스트 요청후 데이터 처리 하는 로직
        url = reverse('posts:post_create')
        # 이 함수는 테스트를 위해서 굳이 우리서버 사진 안올리고 코드가지고 테스팅
        image = SimpleUploadedFile("test.jpg", b"whatevercontents")
        # 요청 이후 받은 결과값이 되겟음
        response = self.client.post(
            url,
            {"image": image, "caption": "test test"}
        )
        #요청이후 받은 결과값이 같은 결과인가 200번 코드 받냐
        self.assertEqual(response.status_code, 200)
        # 전송되는 페이지가 basehtml인가
        self.assertTemplateUsed(response, 'posts/base.html')

    # 사용자가 로그인 하지 않으면 유저 메인으로 이동되는데 그거 테스트
    def test_post_post_create_not_login(self):
        # 포스트 요청후 데이터 처리 하는 로직
        url = reverse('posts:post_create')
        # 이 함수는 테스트를 위해서 굳이 우리서버 사진 안올리고 코드가지고 테스팅
        image = SimpleUploadedFile("test.jpg", b"whatevercontents")
        # 요청 이후 받은 결과값이 되겟음
        response = self.client.post(
            url,
            {"image": image, "caption": "test test"}
        )
        #요청이후 받은 결과값이 같은 결과인가 200번 코드 받냐
        self.assertEqual(response.status_code, 200)
        # 전송되는 페이지가 basehtml인가
        self.assertTemplateUsed(response, 'users/main.html')
