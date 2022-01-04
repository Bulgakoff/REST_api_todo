from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from .models import Article, Project, ToDo, User


# class ArticleSerializer(ModelSerializer):
#     class Meta:
#         model = Article
#         fields = '__all__'

class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSerializerBase(ModelSerializer):
    # QueryParameterVersioning
    class Meta:
        model = User
        fields = ('username',)



class ProjectSerializerBase(ModelSerializer):
    # QueryParameterVersioning
    class Meta:
        model = Project
        fields = '__all__'


class ProjectModelSerializer(ModelSerializer):
    user_id = UserModelSerializer()

    class Meta:
        model = Project
        fields = "__all__"


class ToDoModelSerializer(ModelSerializer):
    user_id = UserModelSerializer()
    project = ProjectModelSerializer()

    class Meta:
        model = ToDo
        fields = "__all__"
