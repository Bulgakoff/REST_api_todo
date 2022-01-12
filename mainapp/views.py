from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.generics import CreateAPIView, ListAPIView, \
    RetrieveAPIView, DestroyAPIView, UpdateAPIView, \
    get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from .filters import ArticleFilter, ProjectFilter
from .models import Article, Project, ToDo
from rest_framework.response import Response

from .serializer import ProjectModelSerializer, UserModelSerializer, \
    ToDoModelSerializer, ProjectSerializerBase, UserSerializerBase
# ArticleSerializer
from rest_framework.decorators import api_view, renderer_classes, action

from rest_framework.permissions import IsAuthenticated, AllowAny

import logging

log = logging.getLogger('rt')  # service_log из settings.py


# ==============Project===============================
class ProjectLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3


class ProjectLimitOffsetPaginatonViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer
    pagination_class = ProjectLimitOffsetPagination


class ProjectCustomDjangoFilterViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer
    filterset_class = ProjectFilter


class ProjectViewSet(viewsets.ViewSet):
    # permission_classes = [AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    # renderer_classes = [JSONRenderer]

    # serializer_class = ProjectModelSerializer
    queryset = Project.objects.all()

    # QueryParameterVersioning
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ProjectModelSerializer
        return ProjectSerializerBase

    def list(self, request):
        # users = User.objects.all()
        pjes = Project.objects.all()
        serializer = ProjectModelSerializer(pjes, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        pj = get_object_or_404(Project, pk=pk)
        serializer = ProjectModelSerializer(pj)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        pj = Project.objects.create(spam=request.data)
        serializer = ProjectModelSerializer(pj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        pj = Project.objects.get(pk=pk)
        serializer = ProjectModelSerializer(pj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ===== for User (User) ===========================================
# ViewSets (наборы представлений) позволяют объединять
# несколько представлений в один набор.
# /viewsets/viewset/1/article_text_only/

class UserLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 1  # 100


class UserLimitOffsetPaginatonViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    pagination_class = UserLimitOffsetPagination


class UserViewSet(viewsets.ViewSet):
    # permission_classes = [permissions.IsAuthenticated]  # ТО drf смотрит в
    # header['authorisation'] и ищет там токен и проверять его в базе
    # permission_classes = [AllowAny]
    # renderer_classes = [JSONRenderer]
    #
    # serializer_class = UserModelSerializer
    queryset = User.objects.all()

    # QueryParameterVersioning
    # def get_serializer_class(self):  # как отрабатывает эта функция?
    #     print(f'--------------=>>>>>>>>>{self.request}')
    #     if self.request.version == '2.0':
    #         return UserSerializerBase
    #     return UserModelSerializer

    def list(self, request):  # без определения функций list, retrieve ... не работает
        """
        # Заголовок первого уровня #
            ## Заголовок h2
            ### Заголовок h3
            #### Заголовок h4
            ##### Заголовок h5
            ###### Заголовок h6

        :param request:  request request request
        :return:
        """

        users = User.objects.all()
        if self.request.version == '2.0':
            serializer = UserSerializerBase(users, many=True)
        else:
            serializer = UserModelSerializer(users, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserModelSerializer(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = User.objects.create(username=request.data, *args, **kwargs)
        serializer = UserModelSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = User.objects.get(pk=pk)
        serializer = UserModelSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserCustomViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin,
                        mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    # ===========ToD o=======================


class TodoViewSet(viewsets.ViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    # renderer_classes = [JSONRenderer]
    serializer_class = ToDoModelSerializer
    queryset = ToDo.objects.all()


    def list(self, request):
        todoes = ToDo.objects.all()
        serializer = ToDoModelSerializer(todoes, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        todo = get_object_or_404(ToDo, pk=pk)
        serializer = ToDoModelSerializer(todo)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            todo = ToDo.objects.get(pk=pk)
        except ToDo.DoesNotExist:
            raise ValueError
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        todo = ToDo.objects.create(request.data, *args, **kwargs)
        serializer = ToDoModelSerializer(todo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        todo = ToDo.objects.get(pk=pk)
        serializer = ToDoModelSerializer(todo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TodoModelViewSet(viewsets.ModelViewSet):
    # renderer_classes = [JSONRenderer]
    queryset = ToDo.objects.all()
    serializer_class = ToDoModelSerializer


class TodoLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20  # 100


class TodoLimitOffsetPaginatonViewSet(viewsets.ModelViewSet):
    queryset = ToDo.objects.all()
    serializer_class = ToDoModelSerializer
    pagination_class = TodoLimitOffsetPagination


# по полю Project
class TodoDjangoFilterViewSet(viewsets.ModelViewSet):
    queryset = ToDo.objects.all()
    serializer_class = ToDoModelSerializer
    filterset_fields = ['project']

# class ArticleAPIVIew(APIView):
#     renderer_classes = [JSONRenderer]
#
#     def get(self, request, format=None):
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         log.warning(f'===>{request.data}---->{request.POST}')
#         return Response(serializer.data)


# @api_view(['GET'])
# @renderer_classes([JSONRenderer])
# def article_view(request):
#     articles = Article.objects.all()
#     serializer = ArticleSerializer(articles, many=True)
#     return Response(serializer.data)


# CreateAPIVIew ---- >Generic
# class ArticleCreateAPIView(CreateAPIView):
#     renderer_classes = [JSONRenderer]
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer


# ListAPIView
# class ArticleListAPIView(ListAPIView):
#     renderer_classes = [JSONRenderer]
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer


# RetrieveAPIView
# class ArticleRetrieveAPIView(RetrieveAPIView):
#     renderer_classes = [JSONRenderer]
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#

# DestroyAPIView
# class ArticleDestroyAPIView(DestroyAPIView):
#     renderer_classes = [JSONRenderer]
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer


# UpdateAPIVIew
# class ArticleUpdateAPIView(UpdateAPIView):
#     renderer_classes = [JSONRenderer]
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer


# ViewSets (наборы представлений) позволяют объединять
# несколько представлений в один набор.
# /viewsets/viewset/1/article_text_only/
# class ArticleViewSet(viewsets.ViewSet):
#     renderer_classes = [JSONRenderer]
#
#     @action(detail=True, methods=['get'])
#     def article_text_only(self, request, pk=None):
#         article = get_object_or_404(Article, pk=pk)
#         return Response({'article.text': article.text})
#
#     def list(self, request):
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         article = get_object_or_404(Article, pk=pk)
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)


# ModelViewSet вообще все сразу весь  CRUD
# class ArticleModelViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     renderer_classes = [JSONRenderer]
#     serializer_class = ArticleSerializer


# Custom ViewSet
# class ArticleCustomViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
#                            mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer]


# get_queryset         Filter
# class ArticleQuerysetFilterViewSet(viewsets.ModelViewSet):
#     serializer_class = ArticleSerializer
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
#     queryset = Article.objects.all()
#
#     def get_queryset(self):
#         return Article.objects.filter(name__contains='123')


#  kwargs
# class ArticleKwargsFilterView(ListAPIView):
#     serializer_class = ArticleSerializer
#
#     def get_queryset(self):
#         name = self.kwargs['name']
#         return Article.objects.filter(name__contains=name)


# Параметры запроса
# class ArticleParamFilterViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#
#     def get_queryset(self):
#         name = self.request.query_params.get('name', '')
#         articles = Article.objects.all()
#         if name:
#             articles = articles.filter(name__contains=name)
#         return articles


# Параметры DjangoFilter
# class ArticleDjangoFilterViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     filterset_fields = ['name', 'user']


# class ArticleCustomDjangoFilterViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     filterset_class = ArticleFilter


# Pagination LimitOffsetPagination
# class ArticleLimitOffsetPagination(LimitOffsetPagination):
#     default_limit = 100


# class ArticleLimitOffsetPaginatonViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     pagination_class = ArticleLimitOffsetPagination
