# OPENCURTAIN DJANGO 서버

제주대학교 컴퓨터공학전공 전시회에 제출할 **오픈커튼**앱에서 사용할 서버를 django로 만들었습니다.

## 사용한 오픈소스
 - [Django](https://github.com/django/django)
 - [Django REST Framework](https://github.com/encode/django-rest-framework)


## 기능
1. 학교 전자메일 인증을 하여 회원가입
2. 학교, 단과대학, 학과(전공)별로 게시판 제공
3. 사용자가 등록한 대학, 단과대학, 학과의 게시판을 제공
4. 타 대학, 단과대학, 학과의 게시판을 추가로 구독하여 게시판 이용 가능
5. 게시판에 글을 작성할 수 있으며, 해당 글에 댓글도 작성 가능
6. 클라이언트(Android, iOS)와 통신을 할때 RESTful 방식으로 JSON 데이터를 주고 받음

## 필요한 것
- Python >= 3.7+
- Django >= 2.2+
- Django REST Framework >= 3.9+

## 문서

- **master** : 안정화 된 서버의 버전들을 제공할 브랜치입니다.
- **develop** : 현재 개발중인 내용들이 적용되는 브랜치입니다. 아직 불안정한 부분이 많이 있습니다.

이 프로젝트에 도움을 주고싶다면 언제든지 PR을 보내주세요. 환영합니다.


## 빠른 시작
    $ git clone https://github.com/noion0511/opencurtain.git
    $ python3 -m venv env
    $ source env/bin/activate (윈도우즈에서는 env/Scripts/activate)
    (env) $ pip install django
    (env) $ pip install djangorestframework
    (env) $ cd opencurtain
    (env) $ python manage.py makemigrations
    (env) $ python manage.py migrate
    (env) $ python manage.py runserver
