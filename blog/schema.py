import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from mainapp.models import Project, ToDo

# class Query(graphene.ObjectType):
#     hello = graphene.String(default_value="Hi!")
#
#
# schema = graphene.Schema(query=Query)

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = '__all__'


class TodoType(DjangoObjectType):
    class Meta:
        model = ToDo
        fields = '__all__'


class Query(graphene.ObjectType):
    all_projects = graphene.List(ProjectType)
    all_todoes = graphene.List(TodoType)
    all_users = graphene.List(UserType)

    user_by_id = graphene.Field(UserType, id=graphene.Int(required=True))

    todoes_by_user_username = graphene.List(TodoType, username=graphene.String(required=False))

    def resolve_todoes_by_user_username(self, info, username=None):
        todoes = ToDo.objects.all()
        if username:
            todoes = todoes.filter(user_id__username=username)
        return todoes

    def resolve_user_by_id(self, info, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None

    def resolve_all_projects(root, info):
        return Project.objects.all()

    def resolve_all_todoes(root, info):
        return ToDo.objects.all()

    def resolve_all_users(root, info):
        return User.objects.all()


schema = graphene.Schema(query=Query)
