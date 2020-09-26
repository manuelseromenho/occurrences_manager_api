# from drf_extra_fields.geo_fields import PointField
from drf_extra_fields.geo_fields import PointField

from occurrences.models import Occurrence, Category
from rest_framework import serializers
from django.contrib.auth import get_user_model # If used custom user model

UserModel = get_user_model()


class OccurrenceSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = serializers.SlugRelatedField(
        read_only=False,
        queryset=Category.objects.all(),
        slug_field='type'
    )
    geo_location = PointField()

    class Meta:
        model = Occurrence
        fields = ('url', 'id', 'author', 'geo_location', 'description',
                  'created', 'updated', 'status', 'category')

    def create(self, validated_data):
        return Occurrence.objects.create(**validated_data)


class CreateAuthorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        fields = ('url', 'id', 'username', 'password')


class AuthorSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='username')
    occurrences = serializers.PrimaryKeyRelatedField(many=True, queryset=Occurrence.objects.all())

    class Meta:
        model = UserModel
        fields = ('url', 'id', 'author', 'occurrences')

    def get_author(self, obj):
        return obj.author.username
