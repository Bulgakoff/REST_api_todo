from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.contrib import admin
from django.urls import path, include, re_path
from graphene_django.views import GraphQLView
from rest_framework import permissions
from rest_framework.authtoken import views

from rest_framework.routers import DefaultRouter

from mainapp.views import TodoModelViewSet, UserCustomViewSet, \
    UserViewSet, TodoViewSet, ProjectViewSet, \
    ProjectCustomDjangoFilterViewSet, \
    TodoDjangoFilterViewSet, \
    ProjectLimitOffsetPaginatonViewSet, \
    UserLimitOffsetPaginatonViewSet, TodoLimitOffsetPaginatonViewSet

# ArticleModelViewSet,  ArticleCustomViewSet,  \
# ArticleViewSet,\
# ArticleQuerysetFilterViewSet, ArticleParamFilterViewSet, \
# ArticleDjangoFilterViewSet, ArticleCustomDjangoFilterViewSet,\
# ArticleLimitOffsetPaginatonViewSet, \
# ArticleAPIVIew, article_view, \
# ArticleCreateAPIView, ArticleListAPIView, \
# ArticleRetrieveAPIView, ArticleDestroyAPIView, ArticleUpdateAPIView, ArticleKwargsFilterView
from userapp.views import UserListAPIView

router = DefaultRouter()
# # router.register('base_model_article', ArticleModelViewSet)
router.register('base_model_MVS_todo_del', TodoModelViewSet)

# # router.register('base_custom_article', ArticleCustomViewSet)
router.register('user_custom', UserCustomViewSet)

# # router.register('base_article', ArticleViewSet, basename='article')  # 111111111111

# router.register('user_base', UserViewSet)
router.register('user_base', UserViewSet, basename='ub')
# router.register('todo_base', TodoViewSet)
router.register('todo_base', TodoViewSet, basename='tb')
# router.register('pj_base', ProjectViewSet)
router.register('pj_base', ProjectViewSet, basename='pb')

filter_router = DefaultRouter()
# # filter_router.register('queryset', ArticleQuerysetFilterViewSet)
# # filter_router.register('param', ArticleParamFilterViewSet)
# # filter_router.register('django', ArticleDjangoFilterViewSet)
# # filter_router.register('custom-django', ArticleCustomDjangoFilterViewSet)
filter_router.register('custom_filter_pj', ProjectCustomDjangoFilterViewSet)
filter_router.register('django_filter_todo', TodoDjangoFilterViewSet)

pagination_router = DefaultRouter()
# # pagination_router.register('pagination_article', ArticleLimitOffsetPaginatonViewSet)
pagination_router.register('pagination_project', ProjectLimitOffsetPaginatonViewSet)
pagination_router.register('pagination_user', UserLimitOffsetPaginatonViewSet)
pagination_router.register('pagination_todo', TodoLimitOffsetPaginatonViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Blog",
        default_version='0.1',
        description="Documentation to out project",
        contact=openapi.Contact(email="admin@admin.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # для GraphQL-запросов:
    path("graphql/", GraphQLView.as_view(graphiql=True)),

    # ViewSets  :
    path('admin/', admin.site.urls),

    # UrlPathVersioning
    re_path(r'^api_version/(?P<version>\d\.\d)/users/$', UserListAPIView.as_view()),
    # NamespaceVersioning
    path('api_version/users/min', include('userapp.urls', namespace='0.1')),
    path('api_version/users/full', include('userapp.urls', namespace='0.2')),

    # Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # ViewSets for router.  :
    path('viewsets/', include(router.urls)),  # 11111111111111111111111111111111111111111

    # path('views/api-view/', ArticleAPIVIew.as_view()),  # # GET принимает
    # path('views/func-api-view/', article_view),
    # generics  :
    # path('generic/create/', ArticleCreateAPIView.as_view()),  # post принимает данные
    # path('generic/list/', ArticleListAPIView.as_view()),  # получает весь список данных что есть у данной view

    # path('generic/retrieve/<int:pk>/', ArticleRetrieveAPIView.as_view()),
    # get получает данные об одном из списка
    # path('generic/destroy/<int:pk>/', ArticleDestroyAPIView.as_view()),
    # path('generic/update/<int:pk>/', ArticleUpdateAPIView.as_view()),
    # filters
    path('filters/', include(filter_router.urls)),
    # path('filters/kwargs/<str:name>/', ArticleKwargsFilterView.as_view()),
    # Pagination
    path('pagination/', include(pagination_router.urls)),

    path('api-token-auth/', views.obtain_auth_token)

]
