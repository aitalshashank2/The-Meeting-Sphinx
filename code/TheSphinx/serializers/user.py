from rest_framework.serializers import ModelSerializer
from TheSphinx.models.user import User


class UserPostSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'full_name',
            'profile_picture',
            'email',
        ]
        read_only_fields = ['id', ]


class UserGetSerializer(ModelSerializer):
    class Meta:
        model = User
        depth = 1
        fields = [
            'id',
            'full_name',
            'profile_picture',
            'email',
        ]
        read_only_fields = [
            'id',
            'full_name',
            'profile_picture',
            'email',
        ]
