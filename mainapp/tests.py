import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, \
    APISimpleTestCase, APITestCase
from mixer.backend.django import mixer
from .views import UserViewSet, ProjectViewSet, TodoViewSet
from django.contrib.auth.models import User
from .models import Project, ToDo


class TestUserViewSet(TestCase):

    def test_get_list(self):
        factory = APIRequestFactory()
        request = factory.get('/viewsets/user_base/')
        view_list = UserViewSet.as_view({'get': 'list'})
        response = view_list(request)
        print(f'=====test_get_list==1===APIRequestFactory=====>response.status_code---- {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_guest(self):  # post запрос без авторизации
        factory = APIRequestFactory()
        request = factory.post('/viewsets/user_base/', {'username': 'Slava'}, format='json')
        view_post = UserViewSet.as_view({'post': 'create'})
        response = view_post(request)
        print(f'=====test_create_guest==2=======>response.status_code---- {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_admin(self):  # не сработал (200 прилетел)
        factory = APIRequestFactory()
        request = factory.post('/viewsets/user_base/', {'username': 'Pushkin'}, format='json')
        admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123456789')
        force_authenticate(request, admin)
        view = UserViewSet.as_view({'post': 'create'})
        response = view(request)
        print(
            f'==status.HTTP_201_CREATED===test_create_admin=3=(force_authenticate)======>response.status_code---- {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED),  # 200 прилетел ????

    def test_get_detail(self):
        user = User.objects.create(username='Push_kin')

        client = APIClient()
        response = client.get(f'/viewsets/user_base/{user.id}/')
        print(f'=====test_get_detail=4=======>response.status_code---- {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_guest(self):
        user = User.objects.create(username='Пушкин')

        client = APIClient()
        response = client.put(f'/viewsets/user_base/{user.id}/', {'username': 'Грин'})
        print(f'=====test_edit_guest=5  =======>response.status_code---- {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_admin(self):  # пример полноценного теста
        # 6.
        user = User.objects.create(username='Вася')

        client = APIClient()
        print(f'===  6 =-++++-- {user}')
        admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admi123456789')
        client.login(username='admin', password='admi123456789')
        response = client.put(f'/viewsets/user_base/{user.id}/', {'username': 'Грин', 'is_active': True})
        print(f'===  6 =test_edit_admin=4======>response.status_code---- {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(id=user.id)
        print(f'===  6 =--- {user.username}')
        self.assertEqual(user.username, 'Грин')
        print(f'===  6 =--- {user.is_active}')
        self.assertEqual(user.is_active, True)
        client.logout()


# =================== APISimpleTestCase ===========================================

class TestMath(APISimpleTestCase):  # используетсчя мало
    def test_sqrt(self):
        import math
        self.assertEqual(math.sqrt(4), 2)


# =================== APITestCase ===========================================
class TestProjectViewSet(APITestCase):

    def test_get_list(self):
        response = self.client.get('/viewsets/pj_base/')
        print(f'===  7  =TestProjectViewSet (APITestCase) --- {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_admin_1(self):
        user = User.objects.create(username='Пушкин', last_name='Vasia')
        project = Project.objects.create(name='Учеба', user_id=user)

        admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123456')
        self.client.login(username='admin', password='admin123456')
        print(f' test_edit_admin_1  > before >>> {project.name}')
        response = self.client.put(f'/viewsets/pj_base/{project.id}/',
                                   {'name': 'Образование', 'user_id': project.user_id.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)  #
        project = Project.objects.get(id=project.id)
        self.assertEqual(project.name, 'Образование')
        print(f' test_edit_admin_1  > after >>> {project.name}')

    def test_edit_admin_2(self):
        user = User.objects.create(username='Пушкин', last_name='Vasia')
        project = Project.objects.create(name='Учеба', user_id=user)
        todo = ToDo.objects.create(text='Сдать_дз1', user_id=user, project=project)

        admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123456')
        self.client.login(username='admin', password='admin123456')
        response = self.client.put(f'/viewsets/todo_base/{todo.id}/', {'text': 'Сдать_дз2', 'user_id': todo.user_id.id,
                                                                       'project': todo.project.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo = ToDo.objects.get(id=todo.id)
        print(f'------test_edit_admin_2---------------> {todo.text}')
        print(f'==test_edit_admin_2=  9  =TestProjectViewSet (APITestCase) --- {response.status_code}')
        self.assertEqual(todo.text, 'Сдать_дз2')

    def test_edit_mixer(self):
        from faker import Faker
        project = mixer.blend(Project)
        # f = Faker()
        # user = User.objects.create(username=f.name, last_name=f.last_name)
        # project = Project.objects.create(name=f.name, user_id=user)

        # user = User.objects.create(username='Пушкин', last_name='Vasia')
        admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123456')
        self.client.login(username='admin', password='admin123456')
        response = self.client.put(f'/viewsets/pj_base/{project.id}/', {'name': 'Учеба', 'user_id': project.user_id.id})
        print(f'==1 >>>>было >>>=  {project.name}  =test_edit_mixer (APITestCase) --- {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  #
        proj = Project.objects.get(id=project.id)
        print(f'==2 >>стало >>>>>=  {proj.name}  =test_edit_mixer (APITestCase) --- {response.status_code}')
        self.assertEqual(proj.name, 'Учеба')

    def test_get_detail(self):
        pj = mixer.blend(Project, name='Учеба') # проверяем определенную категорию(тему, книгу , проект)

        response = self.client.get(f'/viewsets/pj_base/{pj.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f'=== ;;type.response.contentj ;;;;;;;;;;;;;;;;> {response.content}')  # class 'bytes
        response_pj = json.loads(response.content)
        print(f'=== ;;type.response_pj ;;;;;;;;;;;;;;;;> {type(response_pj)}')  # <class 'dict'>
        print(f'=== >>>>> test_get_detail (TestProjectViewSet(APITestCase)) -{response_pj}-- {response.status_code}')
        self.assertEqual(response_pj['name'], 'Учеба')

    def test_get_detail_user(self):
        pj = mixer.blend(Project, user_id__username='Грин') # обращение по  FK к главной таблице к пользователю

        response = self.client.get(f'/viewsets/pj_base/{pj.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_pj = json.loads(response.content)
        print(f'=== >>>+++>> test_get_detail_author (TestProjectViewSet(APITestCase))'
              f' -{response_pj}-- {response.status_code}')
        self.assertEqual(response_pj['user_id']['username'], 'Грин')
